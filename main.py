# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.

def print_df():
    gen_data = {'name': 'kxg', 'age': 30, 'sex': 'male'}
    df = pd.DataFrame.from_dict(gen_data,orient='index')
    print(df)

def print_work_day():
    d = pd.bdate_range('20210420', '20210529', freq='B')
    d = pd.DataFrame(d, columns=['时间'])
    print(d)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_work_day()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
