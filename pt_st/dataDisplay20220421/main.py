import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import f1_score, precision_score, recall_score
import main_db
import xgb
from PIL import Image

st.set_page_config('数据统计分析')

user_pass = {'10000': 'aaaaaa', '20000': 'bbbbbb', '30000': 'cccccc', '40000': 'dddddd', '50000': 'eeeeee'}


def login_user(userid, password):
    if userid is not None:
        if user_pass.get(userid) == password:
            return True
        else:
            st.warning('用户密码错误请确认后再重试！')
    else:
        st.warning('用户id不可为空！')


@st.cache(allow_output_mutation=True)
def get_df_from_db():
    df_db = main_db.get_df_from_mysql()
    return df_db


df = get_df_from_db()
pre_act_tag = pd.read_csv('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/dataDisplay20220421/pre_act_tag.csv')
# df = pd.read_csv('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/dataDisplay20220421/data.csv')
perc = [.20, .40, .60, .80]
dfd = df.describe(percentiles=perc).round(4)


# 数据列自动分组
def split_data_agg(df_db, df_dfd, field):
    bins = list(set(df_dfd[field][3:10].to_list()))
    bins.sort()
    labels = []
    for i in range(0, len(bins)):
        if i == 0:
            continue
        elif i < len(bins):
            # print(str(bins[i - 1]) + '=<X<' + str(bins[i]))
            labels.append(str(bins[i - 1]) + '=<X<' + str(bins[i]))
    new_field = field + '_type'
    df_db[new_field] = pd.cut(
        df_db[field],
        bins,
        right=False,
        labels=labels)
    new_df = df_db[[new_field, field]]
    new_df_agg = new_df.groupby([new_field])[field].agg('count').reset_index()
    return new_df_agg


# 将volt列分组之后统计每个类别数量，做玫瑰图
df_volt = split_data_agg(df, dfd, 'total_volt')
# 按照soc的大小做气泡图，横纵坐标数量和数据值大小
df_soc = df.groupby(['standard_soc'])['total_volt'].agg('count').reset_index()
# 电流和电压值放一张图做条形图和折线图
df_current_volt = df.groupby(['yr_modahrmn', 'total_current', 'total_volt'])['message_type'].agg('count').reset_index()
df_current_volt['dt'] = df_current_volt['yr_modahrmn'].apply(lambda x: str(x).split(' ')[0])
df_current_volts = df_current_volt.groupby(['dt'])['total_current', 'total_volt'].agg('mean').reset_index()
df_current_volts = df_current_volts[df_current_volts['dt'] >= '2020/4/20']
# 圆环图统计各个tag
df_tag = df.groupby(['tag'])['message_type'].agg('count').reset_index()


def fig_pie(df_tag):
    fig = plt.figure(figsize=(10, 6))  # 创建画布
    # create data
    # 创建数据
    names = df_tag['tag'].to_list()
    size = df_tag['message_type'].to_list()
    # Give color names
    # 画饼图，label设置标签名，colors代表颜色
    plt.pie(size, labels=names, colors=['skyblue', 'green', 'yellow', 'red', 'pink']
            , wedgeprops=dict(width=0.3, edgecolor='w'))
    # 设置等比例轴，x和y轴等比例
    plt.axis('equal')
    plt.text(0.1, 1.1, 'tag')
    return fig


def fig_line_bar(df_current_volts):
    matplotlib.rc("font", family='Heiti TC')  # 用来正常显示中文标签
    # fmt = '%.2f%%'
    # yticks = mtick.FormatStrFormatter(fmt)  #设置百分比形式的坐标轴
    fig = plt.figure(figsize=(60, 20))
    label = '电流电压分布图'
    plt.title(label)
    ax1 = fig.add_subplot(111)
    l = [i for i in range(df_current_volts.shape[0])]
    b = df_current_volts['total_current'].tolist()
    # b=[round(item*100,1) for item in b]

    a = df_current_volts['total_volt'].tolist()
    lx = df_current_volts['dt'].tolist()
    ax1.plot(l, b, 'blue', label=u'电流');
    # ax1.yaxis.set_major_formatter(yticks)

    for i, (_x, _y) in enumerate(zip(l, b)):
        plt.text(_x, _y, a[i], color='black', fontsize=10, )  # 将数值显示在图形上
    # ax2.legend(loc=1)
    ax2 = ax1.twinx()  # this is the important function
    plt.bar(l, a, alpha=0.6, color='brown', label=u'电压')
    ax2.legend(loc=2)
    # ax2.set_ylim([0, 2500])  #设置y轴取值范围
    for i, (_x, _y) in enumerate(zip(l, a)):
        plt.text(_x, _y, str(b[i]) + '%', color='black', fontsize=10, )  # 将数值显示在图形上
    # plt.legend(prop={'family':'SimHei','size':8},loc="upper left")
    plt.xticks(l, lx)
    return fig


def fig_scat(df_soc):
    fig = plt.figure(figsize=(10, 6))  # 创建画布
    s = list(df_soc.total_volt / 10)
    # 气泡颜色
    color = np.random.rand(len(list(df_soc.standard_soc)))
    # print(color)
    # 绘制
    plt.scatter(x=list(df_soc.standard_soc), y=list(df_soc.total_volt), s=s, c=color)
    plt.xlabel('standard_soc')
    plt.ylabel('number')
    # plt.title('Scatter')
    return fig


def fig_dat(pdat):
    matplotlib.rc("font", family='Heiti TC')
    # 角度
    l = pdat['total_volt']
    print(l)
    N = pdat.shape[0]  # 总数
    width = 2 * np.pi / N
    rad = np.cumsum([width] * N)  # 每个扇形的起始角度

    # color
    colors = ['blue', 'blueviolet', 'orange', 'brown', 'green', 'pink', 'turquoise', 'tomato']

    fig = plt.figure(figsize=(10, 6))  # 创建画布
    ax = plt.subplot(projection='polar')
    # 删除不必要的内容
    # ax.set_ylim(-4, np.ceil(l.max() + 1))  # 中间空白
    ax.set_theta_zero_location('N')  # 设置极坐标的起点（即0度）在正上方向
    ax.grid(False)  # 不显示极轴
    ax.spines['polar'].set_visible(False)  # 不显示极坐标最外的圆形
    ax.set_yticks([])  # 不显示坐标间隔
    ax.set_thetagrids([])  # 不显示极轴坐标
    # 绘画
    ax.bar(rad, l, width=width, color=colors, alpha=1)
    # text
    for i in np.arange(N):
        ax.text(rad[i] + 0.08,  # 角度
                l[i],  # 长度
                pdat['total_volt_type'][i],  # 文本
                rotation=rad[i] * 180 / np.pi,  # 文字角度
                rotation_mode='anchor',  # this parameter is a trick
                alpha=1,
                fontweight='bold', size=12
                )
    return fig


# 前端展示部分


menu = ['登录', '可视化', '预测']
if 'count' not in st.session_state:
    st.session_state.count = 0

choice = st.sidebar.selectbox("功能选项", menu)
st.sidebar.markdown(
    """
 <style>
 [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
     width: 300px;
 }
 [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
     width: 200px;
     margin-left: -250px;
 }
 </style>
 """,
    unsafe_allow_html=True, )

if choice == "登录":
    st.sidebar.subheader("登录区域")
    userid = st.sidebar.text_input("用户id")
    password = st.sidebar.text_input("密码", type="password")
    if st.sidebar.button("开始登录"):
        logged_user = login_user(userid, password)
        if logged_user:
            st.session_state.count += 1
            if st.session_state.count >= 1:
                st.sidebar.success("您已成功登录！")
                st.balloons()
                st.title("数据展示 ☕ ")
        else:
            st.session_state.count = 0
elif choice == '可视化':
    if st.session_state.count >= 1:
        c1, _, c2 = st.columns([10, 3, 10])
        with c1:
            st.header('数据图表')
            tables = ['玫瑰图', '气泡图', '柱线图', '圆环图', '选择一张图']
            tables1 = ['玫瑰图', '气泡图', '柱线图', '圆环图']
            table = st.selectbox('', tables, index=len(tables) - 1).split()[0]
            if table == '玫瑰图':
                st.write('total_volt 数值分布玫瑰图')
                st.pyplot(fig_dat(df_volt))
            elif table == '气泡图':
                st.write('standard_soc 数值分布气泡图')
                st.pyplot(fig_scat(df_soc))
            elif table == '柱线图':
                st.write('total_current,total_volt 数值分布柱线图')
                st.pyplot(fig_line_bar(df_current_volts))
            elif table == '圆环图':
                st.write('tag 数值分布圆环图')
                st.pyplot(fig_pie(df_tag))
        with c2:
            st.header('搜索')
            num = st.number_input("选取数值", 1, 300, 50, 1)
            if st.button('开始搜索total_volt的数量'):
                query = df[df['total_volt'] >= num].shape[0]
                st.write("total_volt 大于" + str(num) + '的数据有：')
                st.write(query)
elif choice == '预测':
    if st.session_state.count >= 1:
        st.header('分析预测')
        st.subheader('相关性分析')
        st.pyplot(xgb.fig_corr())
        mnames = ['svm&xgb', 'LSTM模型']
        mname = st.selectbox('选择模型分析', mnames)
        c1, _, c2 = st.columns([10, 1, 10])
        if mname == 'svm&xgb':
            with c1:
                st.subheader('预测值对比')
                st.dataframe(xgb.get_pred_df())
            with c2:
                st.subheader('模型评估对比')
                st.pyplot(xgb.fig_xgb())
                st.subheader('harging status')
                harging_status_image = Image.open('pt_st/dataDisplay20220421/harging status.png')
                st.image(harging_status_image)
                st.subheader('vehicle state')
                vehicle_state_image = Image.open('pt_st/dataDisplay20220421/vehicle_state.png')
                st.image(harging_status_image)
        elif mname =='LSTM模型':
            with c1:
                st.subheader('预测值与实际值对比')
                st.dataframe(pre_act_tag[['预测tag', '实际tag']])
            with c2:
                st.subheader('模型评估')
                y_pred = np.array(pre_act_tag['预测tag'])
                y_true = np.array(pre_act_tag['实际tag'])
                f1 = f1_score(y_true, y_pred, average='macro')
                p = precision_score(y_true, y_pred, average='macro')
                r = recall_score(y_true, y_pred, average='macro')
                st.metric(label="F1值:", value=f1, delta_color="inverse")
                st.metric(label="准确率:", value=p, delta_color="inverse")
                st.metric(label="召回率:", value=r, delta_color="inverse")
