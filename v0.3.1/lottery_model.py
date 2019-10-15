"""
可信彩票系统

Version: 0.3.1
Author: 老余
Date: 2019-10-15

使用示例：

#文件名：lottery_model.data
01 04 15 17 27 30|11 45147094
01 09 23 26 28 32|06 51216395
02 03 04 08 13 24|14 24179457
02 19 22 23 27 30|08 63744476
03 04 13 19 27 31|11 55628140
05 12 15 16 25 26|07 19384525
05 12 15 16 25 26|07 55617200
06 11 22 26 30 31|05 50115587
08 11 14 24 29 32|03 13070881
08 17 18 19 21 32|09 45147094


D:\>python lottery_model.py lottery_model.data -d 0000000F -n 1
文件名： lottery_model.data
哈希值： 7ee4d882d67a137ec571cb52862a334f01087c626703bcc5a2dc371a83841aff
立即公证和公开该哈希值，并提供lottery_model.data文件的下载

15:13:34 寻找1个满足难度值为'0000000F'的Nonce值...
00000008907c466764e0acdc726baad23beff875a28cd8e491efa8c6ba5404bd 156229769

15:21:29 找到最小的哈希值对应的Nonce = 156229769, 使:
hash('7ee4d882d67a137ec571cb52862a334f01087c626703bcc5a2dc371a83841aff'+'156229769')
='00000008907c466764e0acdc726baad23beff875a28cd8e491efa8c6ba5404bd'

开奖结果为：
09 17 21 25 26 30|13
"""

# !/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from scipy.special import comb
import argparse
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
    print(f'{end_time} 找到最小的哈希值对应的Nonce = {nonce_pool[0][1]}, 使:')
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
    sha256 = hashlib.sha3_256

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
        the_double_chromosphere(nonce, file_hash_sum, HASH=sha256)

        """体彩超级大乐透"""
        # super_lotto(nonce, file_hash_sum, HASH=sha256)

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




