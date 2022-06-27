# -*- codeing = utf-8 -*-
# @Time : 2022/3/31 21:08
# @File : SqliteConnect.py
# @SoftWare : PyCharm


import sqlite3
import numpy as np


def createDataBase():
    conn = sqlite3.connect("data.db")  # 建立数据库连接
    cur = conn.cursor()  # 得到游标对象

    # 表一（存放url id 地址）
    sql_id = '''create table if not exists url_id
    (uid integer primary key ,            
    time DATE)     
    '''

    # 表二（商品信息）
    sql_inf = '''create table if not exists information
    (uid integer primary key , 
    class1 char(32),
    class2 char(32),
    brand char(32),  
    name text,           
    price char(10),
    time DATE
    )          
    '''
    # 表三（历史价格）
    sql_his = '''create table if not exists history
        (id integer primary key autoincrement, 
        uid integer,
        hprice char(10),
        time DATE
        )          
        '''
    cur.execute(sql_id)
    cur.execute(sql_inf)
    cur.execute(sql_his)
    cur.close()
    conn.commit()
    conn.close()


def inserData(data, type):
    try:
        conn = sqlite3.connect("data.db")  # 建立数据库连接
        cur = conn.cursor()
        if type == 1:
            sql = "insert into url_id(uid,time) values(?,?) " \
                  "on  CONFLICT(uid) DO UPDATE SET time = excluded.time"
            cur.execute(sql, data)
        if type == 2:
            sql = "insert into information(uid,class1,class2,brand,name,price,time) \
                values(?,?,?,?,?,?,?) on  CONFLICT(uid) DO UPDATE SET class1 = excluded.class1,class2 = excluded.class2,brand = excluded.brand," \
                  "name = excluded.name,price = excluded.price,time = excluded.time"
            cur.execute(sql, data)
        if type == 3:
            sql = "insert into history(uid,hprice,time) \
                values(?,?,?)"
            cur.execute(sql, data)
    except Exception as e:
        print(e)

        print('插入失败')
        conn.rollback()
        return 0
    else:
        conn.commit()
        print(data)
        pass
    finally:

        cur.close()
        conn.close()


def loadDataBase(typeid, data):
    try:
        conn = sqlite3.connect("data.db")  # 建立数据库连接
        cur = conn.cursor()
        if typeid == 1:
            sql = '''select * from information'''
            if data is not None or len(str(data)) > 0:
                sql = '''select * from information where class1 like '%{0}%' or 
            brand like '%{1}%' or class2 like '%{2}%' '''.format(data, data, data)
            cur.execute(sql)
            datas = cur.fetchall()
            datas = np.array(datas)  # 转array
            datas = datas.tolist()  # 转列表
        elif typeid == 2:
            sql = '''select uid,hprice,time from history'''
            # if data is not None or len(str(data)) > 0:
            #     sql = '''select uid,hprice,time from history where uid = {0} '''.format(data)
            cur.execute(sql)
            datas = cur.fetchall()
            datas = np.array(datas)  # 转array
            datas = datas.tolist()
        elif typeid == 3:
            cur.execute("select name from information where uid = ?", (data,))
            datas = cur.fetchone()
            datas = np.array(datas)  # 转array
            datas = datas.tolist()  # 转列表
        elif typeid == 4:
            cur.execute("select uid  from url_id where time <= ?", (data,))
            datas = cur.fetchall()
        pass
    except Exception as e:
        print(e)
        print('查询失败')
        conn.rollback()
        return 0
    else:
        conn.commit()
        # print(datas)
        return datas
        pass
    finally:
        cur.close()
        conn.close()


import pandas as pd


def get_prod_data():
    prod_data = loadDataBase(1, '')
    print(prod_data)
    df = pd.DataFrame(list(prod_data), columns=['ID', '一级类目', '二级类目', '品牌', '名称', '价格', '时间'])
    df.to_csv('prod_data.csv')
    return df


def get_hist_data():
    hist_data = loadDataBase(2, '')
    print(hist_data)
    df = pd.DataFrame(list(hist_data), columns=['ID', '历史价格', '时间'])
    # df.to_csv('hist_data.csv')
    return df


if __name__ == '__main__':
    # print(get_hist_data())
    # createDataBase()
    # print(loadDataBase(2,''))
    import matplotlib.pyplot as plt
    df = get_hist_data()
    prod = '4368728'
    sh_df = df[df['ID'] == prod]
    fig = plt.figure(figsize=(10, 6))
    plt.plot(list(sh_df['时间']), list(sh_df['历史价格']), linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('时间')
    plt.ylabel('历史价格')
    plt.title(prod)
    plt.legend()
