#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import itertools
import heapq
from datetime import datetime


def hash_file_data(filename, HASH=hashlib.sha256) -> str:
    """打开文件数据，返回其hash值"""
    with open(filename, 'rt') as f:
        print('文件名：', filename)
        """读取文件并截除头尾空字符"""
        lines = str.strip(f.read())
        origin_hash_sum = HASH(lines.encode()).hexdigest()
        print('哈希值：', origin_hash_sum)
        return origin_hash_sum


def nonce_filter(origin_hash_sum, difficulty='000F', nonce_pool_size=20, HASH=hashlib.sha256):
    """找到满足难度要求的nonce值，使hash(origin_hash_sum + nonce)小于difficulty"""
    """需要记录时间"""
    print(f'')
    start_time = datetime.now().strftime('%X')
    print(f'{start_time} 寻找{nonce_pool_size}个满足难度值为{difficulty!r}的Nonce值...')
    nonce_pool = []
    """这里强行要求nonce值为从0开始的自然数，方便验证工作量"""
    nonce = 0
    while len(nonce_pool) < nonce_pool_size:
        s = origin_hash_sum + str(nonce)
        hash_sum = HASH(s.encode()).hexdigest()
        if hash_sum < difficulty:
            """使用堆压入方式，则第一个元素就是最小值"""
            heapq.heappush(nonce_pool, (hash_sum, nonce))
            print(nonce, end=',')
        nonce += 1
    print('')
    end_time = datetime.now().strftime('%X')
    print(f'{end_time} 其中最小的哈希值对应的Nonce = {nonce_pool[0][1]}, 使:')
    print(f'hash({origin_hash_sum} + {nonce_pool[0][1]})\n={nonce_pool[0][0]}')
    return nonce_pool[0]


def map_lottery_ball(nonce, origin_hash_sum, HASH=hashlib.sha256):
    """把彩票池数据的哈希值和计算出来的nonce值，映射到彩票号码空间"""
    s = str(nonce) + origin_hash_sum
    hash_sum = HASH(s.encode()).hexdigest()
    """6个红球的组合数为1107568, red_balls为这些组合中的中奖号码的序号"""
    red_balls = int(hash_sum, 16) % 1107568
    """篮球为16个中选一个，blue_ball为开奖的篮球号码"""
    blue_ball = int(hash_sum, 16) % 16
    lottery_space = range(1107568)

    for i, c in zip(lottery_space, itertools.combinations(RED_BALLS, 6)):
        if i == red_balls:
            print('')
            print(f'开奖结果为：')
            print(' '.join(c) + "|" + BLUE_BALLS[blue_ball])


if __name__ == '__main__':
    """HASH算法和DIFFICULTY值是开奖算法的核心参数"""
    HASH = hashlib.sha256
    DIFFICULTY = '000000F'

    """以福利彩票的双色球为例，玩法为33个红球中选6个，16个篮球中选一个"""
    RED_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                 '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                 '31', '32', '33')
    BLUE_BALLS = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                  '11', '12', '13', '14', '15', '16')

    """STEP 1
     
    打开彩票池数据，计算其hash值
    彩票池数据是以'\r'分隔的彩票号码，以双色球为例，
    '01 04 15 17 27 30|11'表示6个红球和一个篮球。
    """
    file_name = 'lottery_model.data'
    try:
        origin_hash_sum = hash_file_data(file_name)
    except FileNotFoundError as e:
        print(f'[错误 2] 文件或路径不存在: {file_name}')
        quit(2)

    """STEP 2
    
    计算满足难度要求的Nonce值，用于计算开奖号码
    """
    _, nonce = nonce_filter(origin_hash_sum, difficulty=DIFFICULTY, nonce_pool_size=1)

    """STEP 3
    
    利用nonce值和彩票池的哈希值origin_hash_sum作为输入，计算开奖号码。
    """
    map_lottery_ball(nonce, origin_hash_sum)

