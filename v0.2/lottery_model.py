"""
可信彩票系统

Step1
对彩票购买时间截止点内的所有已销售彩票号码排序，称该数据为【彩票池】。立即公开和公证彩票池
的数据指纹（也称哈希值），并在随后提供彩票池原始数据的下载。注意，需要确保在临近截止时间点
之前有彩票购买记录。
Step2
把彩票池的数据指纹作为输入，使用一个可以消耗特定时间长度的公开的开奖算法，可以得到一组确定
的开奖号码。对于这个特定的开奖算法来说，因为开奖号码由数据指纹唯一确定，数据指纹由彩票池原
始数据唯一确定，所以开奖号码由原始数据唯一确定。

Version: 0.2
Author: 老余
Date: 2019-09-23

使用示例：

D:\> python lottery_model.py lottery_model.data
文件名： lottery_model.data
哈希值： a1bb968b4a47cbcd5fa8691085dd3eb6ebc75f4b23a0f457472561f9d5853538

16:49:09 寻找10个满足难度值为'00003'的Nonce值...
375251,1106220,1196182,1736290,2275718,2701340,3227470,3880506,4739805,4757911,
16:49:17 找到最小的哈希值对应的Nonce = 2275718, 使:
hash('a1bb968b4a47cbcd5fa8691085dd3eb6ebc75f4b23a0f457472561f9d5853538'+'2275718')
='000002e7500efdf2398d79d41e72477400acb60d23b8ed26f4cea25fc7905de0'

开奖结果为：
02 07 08 09 17 25|01

"""

#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from scipy.special import comb
import sys
import hashlib
import itertools
import heapq


def hash_file_data(filename, HASH=hashlib.sha256):
    """打开文件数据，返回其hash值"""
    with open(filename, 'rt') as f:
        print('文件名：', filename)
        """读取文件并截除头尾空字符"""
        lines = str.strip(f.read())
        hash_sum = HASH(lines.encode()).hexdigest()
        print('哈希值：', hash_sum)
        print(f'立即公证和公开该哈希值，并提供{filename}文件的下载')
        return hash_sum


def nonce_filter(origin_hash_sum, difficulty, nonce_pool_size=1, HASH=hashlib.sha256):
    """找到满足难度要求的nonce值，使hash(origin_hash_sum + nonce)小于difficulty"""
    start_time = datetime.now().strftime('%X')
    print('')
    print(f'{start_time} 寻找{nonce_pool_size}个满足难度值为{difficulty!r}的Nonce值...')
    """为了方便结果可验证，这里强行要求nonce值为从0开始的自然数"""
    nonce = 0
    nonce_pool = []
    while len(nonce_pool) < nonce_pool_size:
        """以下部分仅用于原理演示，实际工作的程序应采用并行计算并作大幅优化"""
        s = origin_hash_sum + str(nonce)
        hash_sum = HASH(s.encode()).hexdigest()
        """difficulty值越小，难度越高，随着难度的增加，找到合适的nonce值的时间呈指数增加"""
        if hash_sum < difficulty:
            heapq.heappush(nonce_pool, (hash_sum, nonce))
            print(nonce, end=',')
        nonce += 1
    print('')
    end_time = datetime.now().strftime('%X')
    print(f'{end_time} 找到最小的哈希值对应的Nonce = {nonce_pool[0][1]}, 使:')
    print(f'hash({origin_hash_sum!r}+{str(nonce_pool[0][1])!r})\n={nonce_pool[0][0]!r}')

    """nonce_pool是堆结构，堆顶的元素是最小的元素"""
    return nonce_pool[0]


def map_lottery_ball(nonce, origin_hash_sum, HASH=hashlib.sha256):
    """拼接nonce和彩票池数据的哈希值字符串，进行第二次哈希，并把结果映射到彩票号码空间"""

    """以福利彩票的双色球为例，玩法为33个红球中选6个，16个篮球中选一个"""
    RED_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                 '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                 '31', '32', '33')
    BLUE_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12', '13', '14', '15', '16')
    total_selected = 6
    """comb_count为从所有33个红球中选择6个红球的组合数，等于1107568"""
    comb_count = comb(len(RED_BALLS), total_selected, exact=True)

    s = str(nonce) + origin_hash_sum
    hash_sum = HASH(s.encode()).hexdigest()
    """selected_red_balls代表选中的红球的组合的序号"""
    selected_red_balls = int(hash_sum, 16) % comb_count
    """篮球为16个中选一个，selected_blue_ball为开奖的篮球号码"""
    selected_blue_ball = int(hash_sum, 16) % len(BLUE_BALLS)

    """利用并行迭代的方式找到序号为selected_red_balls的组对应的红球号码"""
    luck_number = "null"
    for n, red_balls in zip(range(comb_count), itertools.combinations(RED_BALLS, total_selected)):
        if n == selected_red_balls:
            """此时对应的red_balls组合，即是开奖号码"""
            luck_number = ' '.join(red_balls) + "|" + BLUE_BALLS[selected_blue_ball]
            break
    print('')
    print(f'开奖结果为：')
    print(luck_number)
    return luck_number


def main(file_name):
    sha256 = hashlib.sha256
    """难度值'00003'在我的PC上大约1秒钟可以找到一个合格的nonce值，在实际工作中需要大幅提高难度值"""
    DIFFICULTY = '00003'
    found_nonces = 10

    try:
        """STEP 1
        打开彩票池数据file_name，计算其hash值
        彩票池数据是以'\r'分隔的彩票号码，以双色球为例，
        '01 04 15 17 27 30|11'表示6个红球和一个篮球。
        """
        file_hash_sum = hash_file_data(file_name, HASH=sha256)

        """STEP 2
        计算满足难度要求的Nonce值，用于计算开奖号码
        """
        _, nonce = nonce_filter(file_hash_sum, difficulty=DIFFICULTY,
                                nonce_pool_size=found_nonces, HASH=sha256)

        """STEP 3
        利用nonce值和彩票池的哈希值origin_hash_sum作为输入，计算开奖号码。
        """
        map_lottery_ball(nonce, file_hash_sum, HASH=sha256)

    except FileNotFoundError:
        print(f'[错误 2] 文件或路径不存在: {file_name}')
        quit(2)
    except Exception as e:
        print(f'[错误 -1] 未知错误{e}')
        quit(-1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(file_name=sys.argv[1])
    else:
        main(file_name='lottery_model.data')

