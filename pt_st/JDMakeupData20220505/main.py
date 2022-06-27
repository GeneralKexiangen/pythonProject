import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np
import pymysql

# 设置网页标题，以及使用宽屏模式
st.set_page_config(
    page_title="美妆"
    ,layout="wide"
)


def get_df_from_mysql():
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''select * from userstable'''
    c.execute(sql)  # 执行SQL语句
    data = c.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = c.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
    print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


udf = get_df_from_mysql()
users = list(udf['username'])
udf_dict = dict(zip(udf['username'], udf['password']))


def login_user(uid, p):
    if uid not in users:
        st.warning('该账号不存在！')
    elif p == udf_dict[uid]:
        return True
    else:
        st.warning('输入的密码账号错误，请核查后再登录！')



def add_user(u, p):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''insert into userstable (username, password) values('{0}','{1}')'''.format(u, p)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


def update_user(ch, u, p):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''update userstable set username = '{0}', password ='{1}' where username = '{2}' '''.format(u, p, ch)
    print('>>>>>>>>', sql)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


def delete_user(ch):
    # load_dict = np.load('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/JDMakeupData20220505/users.npy',
    #                     allow_pickle=True).item()
    # load_dict = dict(load_dict).pop(c)
    # np.save('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/JDMakeupData20220505/users.npy', load_dict)
    # st.success('已成功删除用户！')
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''delete from userstable where username = '{0}' '''.format(ch)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


@st.cache
def get_prod_data():
    df = pd.read_csv('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/JDMakeupData20220505/prod_data.csv')
    names = ['ID', '一级类目', '二级类目', '品牌', '名称', '价格', '时间']
    df = df[names]
    return df


@st.cache
def get_hist_data():
    df = pd.read_csv('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/JDMakeupData20220505/hist_data.csv')
    names = ['ID', '历史价格', '时间']
    df = df[names]
    return df


def fig_line(df, prod):
    matplotlib.rc("font", family='Heiti TC')  # 用来正常显示中文标签
    sh_df = df[df['名称'] == str(prod)]
    fig = plt.figure(figsize=(10, 6))
    x = sh_df['时间_x']
    y = list(sh_df['历史价格'])
    plt.plot(x, y, linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('时间')
    plt.ylabel('历史价格')
    plt.title(prod)
    # plt.legend()
    return fig


prod_df = get_prod_data()
hist_df = get_hist_data()
hist_df = pd.merge(hist_df, prod_df, how='left', on='ID')
print(hist_df)
his_df = hist_df.dropna()
prods = list(set(his_df['名称']))


# 隐藏右边的菜单以及页脚 以及设置背景颜色
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
#root > div:nth-child(1) > div > div > div > div > section.main.css-1v3fvcr.egzxvld1 > div
 {
    background-color: rgb(244 195 205);
} 
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# 左边导航栏
sidebar = st.sidebar.radio(
    "导航栏",
    ("首页", "用户管理", "美妆数据", "数据可视化")
)

if 'count' not in st.session_state:
    st.session_state.count = 0

if sidebar == "首页":
    st.title("登录")
    st.subheader("登录区域")
    userid = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("开始登录"):
        logged_user = login_user(userid, password)
        if logged_user:
            st.session_state.count += 1
            if st.session_state.count >= 1:
                st.sidebar.success("您已成功登录！")
                st.balloons()
                # st.title("美妆数据 ☕ ")
        else:
            st.session_state.count = 0

elif sidebar == "用户管理":
    st.title("用户管理")
    if st.session_state.count >= 1:
        # 将页面分为左半边和右半边
        left, right = st.columns(2)
        # 左半边页面展示部分
        with left:
            st.subheader("查看用户信息")
            if st.button('查看'):
                st.dataframe(udf)
        # 右半边页面展示部分
        with right:
            st.subheader("添加、修改、删除用户")
            user_action = st.selectbox(
                "请选择操作",
                ["添加用户", "修改用户", "删除用户"]
            )
            if user_action:
                with st.form(user_action):
                    if user_action == "添加用户":
                        usr = st.text_input("用户名")
                        psd = st.text_input("密码", type="password")
                        submitted = st.form_submit_button("提交")
                        if submitted:
                            # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                            add_user(usr, psd)
                            st.success("添加成功")
                    elif user_action == "修改用户":
                        user_choice = st.selectbox('选择要修改的用户', users)
                        new_usr = st.text_input('修改后的用户名')
                        new_psd = st.text_input('修改后的密码', type='password')
                        submitted = st.form_submit_button("提交")
                        if submitted:
                            # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                            update_user(str(user_choice), str(new_usr), str(new_psd))
                            st.success("修改成功")

                    else:
                        user_choice = st.selectbox('选择要删除的用户', users)
                        submitted = st.form_submit_button("提交")
                        if submitted:
                            delete_user(user_choice)
                            # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                            st.success("删除成功")
elif sidebar == "美妆数据":
    st.title("美妆数据")
    if st.session_state.count >= 1:
        keyword = st.text_input('输入关键词', '')
        if len(keyword) > 0:
            show_df = prod_df[
                prod_df['一级类目'].str.contains(keyword) | prod_df['二级类目'].str.contains(keyword) | prod_df[
                    '品牌'].str.contains(
                    keyword)]
            st.dataframe(show_df)
        else:
            st.dataframe(prod_df)

elif sidebar == "数据可视化":
    st.title("数据可视化")
    if st.session_state.count >= 1:
        keyword = st.selectbox('选择一个商品', prods)
        if len(keyword) > 0 or keyword is not None:
            st.pyplot(fig_line(his_df, keyword))

