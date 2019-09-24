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

Version: 0.3
Author: 老余
Date: 2019-09-23

使用示例：

D:\>python lottery_model.py lottery_model.data
文件名： lottery_model.data
哈希值： a1bb968b4a47cbcd5fa8691085dd3eb6ebc75f4b23a0f457472561f9d5853538
立即公证和公开该哈希值，并提供lottery_model.data文件的下载

14:43:55 寻找10个满足难度值为'00003'的Nonce值...
000004fa5661701d6540f237de1370dbf399b768da6638ee2710dd8470c57d9b 375251
000014e0576fc7d5934127c1a5a9f52bca9a45542a081cbefce4b7c1a35584aa 1106220
00002c26bba3b33df01fda5054d9d9950d684ce31dbd26ef608628e1468b00a4 1196182
00001caa0e369889a4f863b977cbd6cd3861d16ede6b32e165620c5a16f5f9b7 1736290
000002e7500efdf2398d79d41e72477400acb60d23b8ed26f4cea25fc7905de0 2275718
00002f5f1f84e827fa0ec909a9db03cea24cec9d809b0f54ca5dd86db8ac526a 2701340
00000c2dc1343ae503c839eb16577138a7c3c0d149763cf5e5ea7b6958852dc5 3227470
000011986d8b27433ecff0ceca1dedfcbcc19028ad0a9a8cd081b00eac98f74f 3880506
0000271c106dba710fcdbdd10a2523c4839c38c43ea4338d63dd099e611ba754 4739805
0000261ca586eb9fe477346c1bb5bbc1e2611eed9890e1e27d353522397b1632 4757911
14:44:05 找到最小的哈希值对应的Nonce = 2275718, 使:
hash('a1bb968b4a47cbcd5fa8691085dd3eb6ebc75f4b23a0f457472561f9d5853538'+'2275718')
='000002e7500efdf2398d79d41e72477400acb60d23b8ed26f4cea25fc7905de0'

开奖结果为：
02 07 08 09 17 25|01

"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from scipy.special import comb
import argparse
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


def nonce_filter(origin_hash_sum, difficulty, nonce_pool_size, HASH=hashlib.sha256):
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
            print(hash_sum, nonce)
        nonce += 1
    print('')
    end_time = datetime.now().strftime('%X')
    print(f'{end_time} 其中最小的哈希值对应的Nonce = {nonce_pool[0][1]}, 使:')
    print(f'hash({origin_hash_sum!r}+{str(nonce_pool[0][1])!r})\n={nonce_pool[0][0]!r}')

    """nonce_pool是堆结构，堆顶的元素是最小的元素"""
    return nonce_pool[0]


def map_luck_number(hash_sum, balls, total_selected):
    """把传入的hash_sum映射到开奖号码"""

    comb_count = comb(len(balls), total_selected, exact=True)
    selected_balls = int(hash_sum, 16) % comb_count

    luck_number = "null"
    for n, comb_balls in zip(range(comb_count), itertools.combinations(balls, total_selected)):
        if n == selected_balls:
            """此时对应的comb_balls组合，即是开奖号码"""
            luck_number = ' '.join(comb_balls)
            break
    return luck_number


def the_double_chromosphere(nonce, origin_hash_sum, HASH=hashlib.sha256):
    """福利彩票的双色球为玩法为33个红球中选6个，16个篮球中选一个"""
    RED_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                 '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                 '31', '32', '33')
    BLUE_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12', '13', '14', '15', '16')

    red_balls_selected = 6
    blue_balls_selected = 1

    s = str(nonce) + origin_hash_sum
    hash_sum = HASH(s.encode()).hexdigest()

    luck_number = map_luck_number(hash_sum, balls=RED_BALLS, total_selected=red_balls_selected)
    luck_number2 = map_luck_number(hash_sum, balls=BLUE_BALLS, total_selected=blue_balls_selected)

    print('')
    print(f'开奖结果为：')
    print(luck_number + '|' + luck_number2)


def super_lotto(nonce, origin_hash_sum, HASH=hashlib.sha256):
    """体彩超级大乐透，玩法为前区35选5，后区12选2"""
    front_zone =('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                 '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                 '31', '32', '33', '34', '35')

    back_zone = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12')

    front_zone_selected = 5
    back_zone_selected = 2

    s = str(nonce) + origin_hash_sum
    hash_sum = HASH(s.encode()).hexdigest()

    luck_number = map_luck_number(hash_sum, balls=front_zone, total_selected=front_zone_selected)
    luck_number2 = map_luck_number(hash_sum, balls=back_zone, total_selected=back_zone_selected)

    print('')
    print(f'开奖结果为：')
    print(luck_number + '|' + luck_number2)


def main(file_name, DIFFICULTY:str, n:int):
    sha256 = hashlib.sha256

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
                                nonce_pool_size=n, HASH=sha256)

        """STEP 3
        利用nonce值和彩票池的哈希值origin_hash_sum作为输入，计算开奖号码。
        """

        """福彩双色球"""
        # the_double_chromosphere(nonce, file_hash_sum, HASH=sha256)

        """体彩超级大乐透"""
        super_lotto(nonce, file_hash_sum, HASH=sha256)

    except FileNotFoundError:
        print(f'[错误 2] 文件或路径不存在: {file_name}')
        quit(2)
    except Exception as e:
        print(f'[错误 -1] 未知错误{e}')
        quit(-1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='根据【彩票池】原始数据计算开奖号码')
    parser.add_argument(dest='filename', nargs='?',
                        default='lottery_model.data',
                        help='【彩票池】原始数据文件名')

    parser.add_argument('-d', dest='difficulty',
                        default='00003',
                        help='减小该值会增大难度，延长计算开奖号码的时间')

    parser.add_argument('-n', dest='size',
                        default=10,
                        help='表示找到n个满足difficulty条件的值')

    args = parser.parse_args()

    main(args.filename, args.difficulty, int(args.size))







