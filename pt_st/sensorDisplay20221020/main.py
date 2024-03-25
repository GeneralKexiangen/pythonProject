import random

import streamlit as st
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title='sensor', layout='wide')


def get_data():
    date_data = pd.DataFrame(pd.date_range(start="20221001", end="20221020", freq="s"), columns=['时间'])
    date_data['星期'] = date_data['时间'].apply(
        lambda x: datetime.date(int(str(x)[0:4]), int(str(x)[5:7]), int(str(x)[8:11])).strftime("%a"))
    date_data['日期'] = date_data['时间'].apply(lambda x: str(x)[0:10])
    date_data['月'] = date_data['时间'].apply(lambda x: int(str(x)[5:7]))
    date_data['日'] = date_data['时间'].apply(lambda x: int(str(x)[8:11]))
    date_data['年'] = date_data['时间'].apply(lambda x: int(str(x)[0:4]))
    date_data['时间'] = date_data['时间'].apply(lambda x: str(x)[11:])
    for i in range(1, 4):
        date_data['温度' + str(i)] = date_data['时间'].apply(lambda x: random.randint(-10, 40))
        date_data['湿度' + str(i)] = date_data['时间'].apply(lambda x: random.randint(1, 100))
        date_data['光照' + str(i)] = date_data['时间'].apply(lambda x: random.randint(100, 500))
    for i in range(1, 4):
        date_data['_温度' + str(i)] = date_data['时间'].apply(lambda x: random.randint(-10, 40))
        date_data['_温度变化量' + str(i)] = date_data['时间'].apply(lambda x: random.randint(-5, 5))
        date_data['_湿度' + str(i)] = date_data['时间'].apply(lambda x: random.randint(1, 100))
        date_data['_湿度变化量' + str(i)] = date_data['时间'].apply(lambda x: random.randint(-10, 10))
        date_data['_电导率' + str(i)] = date_data['时间'].apply(lambda x: random.randint(10, 50))
    date_data.to_csv('数据.csv')
    return date_data
    # print(date_data)


# get_data()
#
df = pd.read_excel('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/sensorDisplay20221020/数据.xlsx')
df = df.fillna(0)
df['时间'] = df['时间'].astype(str)
df['日期'] = df['年'].map(str) + '-' + df['月'].map(str) + '-' + df['日'].map(str)
st.title('传感器变化趋势图')
st.write('数据源展示')
st.dataframe(df)
dt = set(df['日期'])
sr = ['传感器' + str(i) for i in range(1, 67)]
c1, c2 = st.columns(2)
with c1:
    dt_choice = st.selectbox('请选择日期', dt)
with c2:
    sr_choice = st.selectbox('请选择传感器', sr)
last_num = sr_choice.replace('传感器', '')
fileds1 = ['湿度', '湿度差', '湿度变化量', '温度', '温度差', '温度变化量', '电导率']
fileds2 = ['湿度', '温度', '光照强度']
if int(last_num) < 55:
    srs = [x + last_num for x in fileds1]
else:
    srs = [x + last_num for x in fileds2]
df_choice = df[df['日期'] == dt_choice]
srs.append('时间')
df_choice = df_choice[srs]
df_choice.set_index('时间', inplace=True)
st.line_chart(df_choice[0:100])
