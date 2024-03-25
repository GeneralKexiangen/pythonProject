import streamlit as st
import streamlit.components.v1 as components
import pymysql
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import squarify
import numpy as np
import re
import jieba
import wordcloud
from pyecharts.charts import Map
from pyecharts import options as opts
import random

st.set_page_config('微博分析')

def random_num_with_fix_total(maxValue, num):
    '''生成总和固定的整数序列
    maxvalue: 序列总和
    num：要生成的整数个数'''
    a = random.sample(range(1, maxValue), k=num - 1)  # 在1~99之间，采集20个数据
    a.append(0)  # 加上数据开头
    a.append(maxValue)
    a = sorted(a)
    b = [a[i] - a[i - 1] for i in range(1, len(a))]  # 列表推导式，计算列表中每两个数之间的间隔
    # b = b.reverse()
    return b


def stopwordslist(stopwords_path):
    stopwords = [line.strip() for line in open(stopwords_path, encoding='UTF-8').readlines()]
    return stopwords


# 常见停用词
chsw = stopwordslist('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/stopword.txt')
ensw = stopwordslist('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/moviesRecommend20220405/stopworde.txt')


# 分词去掉停用词
def cut_words(words_list):
    cuts = []
    i = 1
    for word in words_list:
        if type(word) == type('1'):
            words = jieba.cut(word)
            ws = []
            #             print(i,word)
            i += 1
            for w in words:
                if w not in chsw and w not in ensw:
                    ws.append(w)
            cuts.extend(ws)
    return cuts


def get_df_from_mysql(dn):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="weibo", charset="utf8")
    c = con.cursor()
    sql = '''select * from {0}'''.format(dn)
    c.execute(sql)  # 执行SQL语句
    datas = c.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = c.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in datas], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
    print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


def fig_tree(num):
    # 中文
    matplotlib.rc("font", family='Heiti TC')
    # data
    labels = ['很好', '还可以', '一般', '糟糕', '非常差']
    # income = [3908, 856, 801, 868, 1361]
    income = random_num_with_fix_total(int(num), 5)
    # plot
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    squarify.plot(sizes=income,  # 方块面积大小
                  label=labels,  # 指定标签
                  alpha=0.8,  # 指定透明度
                  value=income,  # 添加数值标签
                  edgecolor='white',  # 设置边界框
                  # linewidth=0.1  # 设置边框宽度
                         )
    # 设置标签大小
    plt.rc('font', size=15)  # 无效！
    # 设置标题大小
    # ax.set_title('博文情绪', fontsize=22)
    # 去除坐标轴
    ax.axis('off')
    # 去除上边框和右边框刻度
    ax.tick_params(top='off', right='off')
    # 显示图形
    # plt.show()
    return fig


def fig_pie_wb_type():
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    matplotlib.rc("font", family='Heiti TC')
    fig = plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    label = ['原创', '转发']  # 定义饼图的标签，标签是列表
    explode = [0.01, 0.01]  # 设定各项距离圆心n个半径
    # values = [400, 700]
    values = list(np.random.randint(0, 1000, size=2))
    colors = ['green', 'pink', 'blue', 'blueviolet', 'orange', 'brown', 'turquoise', 'tomato']
    plt.pie(values
            , explode=explode
            , labels=label
            , autopct='%1.1f%%'
            , colors=colors
            )  # 绘制饼图
    # plt.show()
    return fig


def fig_bar_fans_age():
    fig = plt.figure(figsize=(6, 6))
    label = ['未成年', '青年', '中年', '老年']
    values = list(np.random.randint(0, 50, size=4))
    plt.barh(range(len(values)), values, tick_label=label)
    # plt.show()
    return fig


def fig_pie_fans_emotions():
    # plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    matplotlib.rc("font", family='Heiti TC')
    fig = plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    label = ['高活', '普通', '低活']  # 定义饼图的标签，标签是列表
    explode = [0.01, 0.01, 0.01]  # 设定各项距离圆心n个半径
    values = list(np.random.randint(0, 50, size=3))
    # colors = ['green', 'pink', 'blue', 'blueviolet', 'orange', 'brown', 'turquoise', 'tomato']
    plt.pie(values
            , explode=explode
            , labels=label
            , autopct='%1.1f%%'
            # , colors=colors
            )  # 绘制饼图
    # plt.show()
    return fig


def fig_pie_wb_source():
    matplotlib.rc("font", family='Heiti TC')
    fig = plt.figure(figsize=(6, 6))
    # data = [40, 15, 20]
    data = list(np.random.randint(0, 50, size=3))
    label = ["安卓", "ios", "网页"]
    # 要把离心率设置远一点，怕第二个饼图挡住这个百分率
    plt.pie(data, pctdistance=0.8, labels=label, autopct='%.1f%%')
    # 所谓的环形图，就是再画一个比上个图小的饼图，并且为白色，所以半径要小
    plt.pie([1], radius=0.6, colors='w')
    # plt.legend(label, loc='upper right')
    # plt.show()
    return fig


def fig_line_post(d, p=None):
    from datetime import date, timedelta
    dd = pd.to_datetime(np.arange(0, d)
                        , unit='D'
                        , origin=pd.Timestamp((date.today() + timedelta(days=-d)).strftime("%Y-%m-%d")))
    if d == 1:
        hourList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15',
                    '16', '17', '18', '19', '20', '21', '22', '23']
        dd = []
        for hour in hourList:
            dd.append(hour + ':00')
        dd = np.array(dd)
    date_data = pd.DataFrame(dd, columns=['Date'])
    data1 = None
    if d == 1:
        data = pd.DataFrame(np.random.randint(0, 10, size=24), columns=['发博数量'])
    else:
        if p is not None:
            data = pd.DataFrame(np.random.randint(0, 20, size=d), columns=['点赞数'])
            data1 = pd.DataFrame(np.random.randint(0, 10, size=d), columns=['转发数'])
        else:
            data = pd.DataFrame(np.random.randint(0, 10, size=d), columns=['发博数量'])
    if p is not None:
        df = pd.concat([date_data, data, data1], axis=1)
    else:
        df = pd.concat([date_data, data], axis=1)
    df = df.set_index('Date')
    return df


def fig_wc(cont):
    # matplotlib.rc("font", family='Heiti TC')
    WC = wordcloud.WordCloud(max_words=200
                             , height=600
                             , width=800
                             , background_color='white'
                             , repeat=False
                             , mode='RGBA'
                             , font_path="/System/Library/fonts/PingFang.ttc"
                             )
    # print('>>>>>>', cont)
    con = WC.generate(cont)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(con)
    ax.axis("off")
    return fig


def fig_pie(v, l):
    values = [v]
    labels = [l]

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            # 显示数值
            return '{v:d}'.format(v=val)
            # 同时显示数值和占比的饼图
            # return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

        return my_autopct

    rad = 1
    if l == '关注数':
        rad = 0.5
    fig = plt.figure(figsize=(6, 6))
    plt.pie(values, radius=rad, autopct=make_autopct(values), colors='c')
    plt.title(l)
    # plt.show()
    return fig


def fig_map():
    province = ['北京', '上海', '广东', '山东', '浙江', '四川', '重庆', '湖北']
    # fans = [32, 14, 23, 9, 19, 48, 58, 0]
    # fans = list(np.random.randint(0, 50, size=8))
    fans = random_num_with_fix_total(800, 8)
    # print(fans)
    province_list = [list(z) for z in zip(province, fans)]
    # 将省份和数量输出
    print(province_list)
    c = (
        Map(init_opts=opts.InitOpts(width="1000px", height="600px"))  # 可切换主题
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国关注地区分布"),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=round(max(fans), 0),
                range_text=['关注数量区间:', ''],  # 分区间
                is_piecewise=True,  # 定义图例为分段型，默认为连续的图例
                pos_top="middle",  # 分段位置
                pos_left="left",
                orient="vertical",
                split_number=6  # 分成6个区间
            )

        )
            .add("关注地区分布", province_list, maptype="china")
            .render("关注地区分布.html")
    )

st.title('大V分析 ✌️💁👏🏼😇😎🥸👻🫶🏽☕️❤️‍🩹')

user = get_df_from_mysql('user')
weibo = get_df_from_mysql('weibo')
weibo['content'] = weibo['content'].apply(lambda x: str(x).replace(' ', '').replace('\n', ''))
uid = list(set(user['fid'].to_list()))
uname = list(set(user[user['id'] == user['fid']]['nickname'].to_list()))

name = st.sidebar.selectbox('请选择一位...', uname)
query = st.sidebar.button('开始查询')
if query:
    st.balloons()
    info = user[user['nickname'] == name].reset_index(drop=True)
    wb_info = weibo[weibo['user_id'] == info['id'][0]].reset_index(drop=True)
    print(info)
    print(str(info['nickname']))
    st.header(info['nickname'][0])

    # 展示个人信息
    l, _, r = st.columns([20, 10, 20])
    with l:
        st.error('个人简介：' + info['description'][0])
        st.warning('性别：' + info['gender'][0])
        st.success('生日：' + info['birthday'][0])
        st.info('地址：' + info['location'][0])
    with r:
        st.metric('微博数', info['weibo_num'][0])
        st.metric('粉丝数', info['followers'][0])
        st.metric('关注数', info['following'][0])
    # 个人微博分析
    st.subheader('博文情绪')
    st.pyplot(fig_tree(info['weibo_num'][0]))
    c2, c3 = st.columns(2)
    with c2:
        st.subheader('博文类型')
        st.pyplot(fig_pie_wb_type())
    with c3:
        st.subheader('博文来源')
        st.pyplot(fig_pie_wb_source())
    st.subheader('上周每日活动')
    st.line_chart(fig_line_post(7))
    st.subheader('近一月每日活动')
    st.line_chart(fig_line_post(30))
    st.subheader('近一年每日活动')
    st.line_chart(fig_line_post(365))
    st.subheader('高峰时段')
    st.bar_chart(fig_line_post(1))

    # WordCloud
    c4, c5 = st.columns(2)
    with c4:
        st.subheader('博文词云')
        if len(wb_info) > 0:
            content = wb_info['content'].to_list()
            content_cuts = cut_words(content)
            content_cuts = ' '.join(content_cuts)
            st.pyplot(fig_wc(content_cuts))
        else:
            st.warning('该用户最近没有博文内容。')
    with c5:
        st.subheader('标签词云')
        if len(wb_info) > 0:
            content = wb_info['content'].to_list()
            label_content = re.findall(r'#(.*?)#', str(content))
            content_cuts = cut_words(label_content)
            content_cuts = ['#' + c for c in content_cuts]
            print(content_cuts)
            if len(content_cuts) > 0:
                content_cuts = ' '.join(content_cuts)
                st.pyplot(fig_wc(content_cuts))
            else:
                st.warning('该用户没有发布带标签的博文。')
        else:
            st.warning('该用户最近没有博文内容。')

    st.subheader('近一月每天微博点赞与转发数')
    st.bar_chart(fig_line_post(30, '?'))

    # 粉丝分析
    st.header('关注分析')
    st.subheader('网络规模')
    c6, c7 = st.columns(2)
    with c6:
        st.pyplot(fig_pie(info['followers'][0], '粉丝数'))
    with c7:
        st.pyplot(fig_pie(info['following'][0], '关注数'))
    c8, c9 = st.columns(2)
    with c8:
        st.subheader('关注年龄分布')
        st.pyplot(fig_bar_fans_age())
    with c9:
        st.subheader('关注活跃度分布')
        st.pyplot(fig_pie_fans_emotions())
    fig_map()
    st.subheader('关注地区分布')
    hl = open('关注地区分布.html', encoding='UTF-8').read()
    components.html(hl, height=600, width=1000)

