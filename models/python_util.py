# -*- coding: utf-8 -*-

import datetime

'''
 python 帮组方法
'''


def get_add_8th_str_time(str_time):
    '''
    :param str_time: 字符串时间
    :return: 增加8小时后的字符串时间
    '''

    data_8_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)

    return data_8_time.strftime('%Y-%m-%d %H:%M:%S')