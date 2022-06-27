# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import docx
import pandas as pd
import os
import json

import datetime, time


def lastMonth(detester):
    date = datetime.datetime.strptime(detester, '%Y-%m-%d')
    year = date.year
    month = date.month
    day = date.day
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    if day == 31 and month in (4, 6, 9, 11):
        day = 30
    if day > 28 and month == 2:
        day = 29 if year % 4 == 0 else 28

    last_beginday = datetime.datetime.strptime('%s-%s-%s' % (year, month, day), '%Y-%m-%d')
    last_sameday = datetime.datetime.strptime(
        '%s-%s-%s %s:%s:%s' % (year, month, day, date.hour, date.minute, date.second), '%Y-%m-%d %H:%M:%S')
    last_begin_timestamp = last_beginday.strftime('%Y-%m-%d')
    last_sameday_timestamp = last_sameday.strftime('%Y-%m-%d')
    return last_begin_timestamp

def getFirstAndLastDay(detester):
    import calendar
    date = datetime.datetime.strptime(detester, '%Y-%m-%d')
    year = date.year
    month = date.month
    # 获取当前月的第一天的星期和当月总天数
    weekDay,monthCountDay = calendar.monthrange(year,month)
    # 获取当前月份第一天
    firstDay = datetime.date(year,month,day=1)
    # 获取当前月份最后一天
    lastDay = datetime.date(year,month,day=monthCountDay)
    # 返回第一天和最后一天
    return lastDay

def get_current_day_timestamp():
    time_string = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    timestamp = time.mktime(datetime.datetime.strptime(time_string, "%Y-%m-%d").timetuple())
    return timestamp


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.


def print_df():
    gen_data = {'name': 'kxg', 'age': 30, 'sex': 'male'}
    df = pd.DataFrame.from_dict(gen_data, orient='index')
    print(df)


def print_work_day():
    d = pd.bdate_range('20210420', '20210529', freq='B')
    d = pd.DataFrame(d, columns=['时间'])
    print(d)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # parse_word()
    # path = '/Users/zhiyue/Desktop/PT/NLP/血症紫癜出血贫血/缺铁贫/周海平,缺铁性贫血,调经,失眠.docx'
    # file = docx.Document(path)
    # for p in file.paragraphs:
    #     print(p.text)
    # import pandas as pd
    #
    # df = pd.read_csv('/Users/zhiyue/PycharmProjects/pythonProject/zhiy/zhiy_nb/stopword.txt', encoding='utf-8')
    # print(df.shape)
    print(getFirstAndLastDay('2021-11-01'))
