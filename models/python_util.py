# -*- coding: utf-8 -*-

import datetime
import time

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


def get_add_8th_date_time(str_time):
    '''
    :param str_time: 字符串时间
    :return: 增加8小时后的Datetime
    '''

    data_8_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)

    return data_8_time


def get_time_list(start_time, end_time):
    start_date_time = get_add_8th_date_time(start_time)
    end_date_time = get_add_8th_date_time(end_time)

    days = (end_date_time- start_date_time).days + 1
    time_days = []  # 排班显示时间
    for day in range(days):
        str_to_datetime = start_date_time + datetime.timedelta(days=day)
        time_days.append(str_to_datetime)

    return time_days


def get_time_difference_th(start_time, end_time):
    '''
    :param start_time: 字符串开始时间
    :param end_time: 字符串结束时间
    :return: int 的相差多少小时
    '''
    start_date_time = time.mktime(get_add_8th_date_time(start_time).timetuple())
    end_date_time = time.mktime(get_add_8th_date_time(end_time).timetuple())

    difference_th = round((end_date_time - start_date_time) / (60 * 60), 2)

    return difference_th


def to_morning_difference_th(dtime):
    '''
     到第二天凌晨相差多少小时
    :param dtime: 字符串有时分秒时间
    :return:
    '''
    date_time = datetime.datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')
    morning = datetime.datetime.strptime(dtime[:10], '%Y-%m-%d')
    morning_time = morning + datetime.timedelta(days=1)

    difference_th = round((time.mktime(morning_time.timetuple()) - time.mktime(date_time.timetuple())) / (60 * 60), 2)

    return difference_th

def today_morning_difference_th(dtime):
    '''
     到今天凌晨相差多少小时
    :param dtime: 字符串有时分秒时间
    :return:
    '''
    date_time = datetime.datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')
    morning = datetime.datetime.strptime(dtime[:10], '%Y-%m-%d')
    int_time1 =time.mktime(date_time.timetuple())
    int_time2 = time.mktime(morning.timetuple())

    difference_th = round((int_time1-int_time2)/ (60 * 60), 2)


    return difference_th


print(today_morning_difference_th('2010-10-10 10:00:00'))