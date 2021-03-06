import os
from pprint import pprint

import pymysql

layer_map = {
    # '28-1b20292fb8ff': '顶一里',
    # '28-1b20292fb4ff': '顶一外',
    # '28-1b20293100ff': '顶二里',
    # '28-1b2029314eff': '顶二外',
    '28-1b202933b1ff': '顶三里',
    '28-1b202a4baaff': '一',
    '28-1b202a193fff': '二',
    '28-1b202a23d4ff': '三',
    '28-1b202a298fff': '四',
    '28-1b2029ff4cff': '五',
    '28-1b202a4bdeff': '六',
    '28-1b202a1a49ff': '七',
    '28-1b202a213fff': '八',
    '28-1b202a4bc3ff': '九',
    '28-1b202a2964ff': '十',
    '28-1b2029314eff': '十一',
    '28-1b2029313dff': '十二',
    '28-1b202929c6ff': '十三',
    '28-1b20292fb8ff': '十四',
    '28-1b20292fb4ff': '十五',
    '28-1b20293504ff': '十六',
    '28-1b20293100ff': '十七',
}


def get_cache_html():
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'caches')
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    return {file.split('.')[0] for file in os.listdir(cache_path) if file.endswith('html')}


class Solution:
    """根据yaw值计算门开关时间以及持续时间"""
    yaw_threshold = 15
    count_threshlod = 2

    cnt = 0
    ret = []

    def __init__(self, data=None):
        self.c = pymysql.connect("192.168.2.159", "django", "django", "origin").cursor()
        if data is None:
            self.data = []
        else:
            self.data = data

    def load_db(self, start, end):
        self.c.execute("select `time`, yaw from tbl_door where `time`>=%s and `time`<%s order by `time`", (start, end))
        self.data = self.c.fetchall()

    def judge_open(self, is_open=False, is_close=False):
        """当门的角度超过阙值一定时间间隔粒度，及判断为开门，当阙值小于一定时间间隔粒度，即判断为关门时间"""
        index = 0
        while index < len(self.data):
            cnt = 0
            start, yam = self.data[index]
            if abs(yam) >= self.yaw_threshold:
                while index < len(self.data) and abs(yam) >= self.yaw_threshold:
                    cnt += 1
                    end, yam = self.data[index]
                    index += 1
                if cnt >= self.count_threshlod:
                    self.ret.append((start, end))
            index += 1
        self.show_ret()

    def show_ret(self):
        serial_number = 1
        for start, end in self.ret:
            print(serial_number, '%s----%s' % (start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')), '持续时间：%s' % (end - start).seconds)
            serial_number += 1


if __name__ == '__main__':
    sol = Solution()
    sol.load_db('2020-09-02 00:00:00', '2020-09-03 00:00:00')
    sol.judge_open()
