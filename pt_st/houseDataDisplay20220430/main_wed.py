import main_db
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import statsmodels.api as sm
import warnings
import streamlit as st
import streamlit.components.v1 as components

warnings.filterwarnings("ignore")


@st.cache
def get_data():
    dt = main_db.get_df_from_mysql('shuju')
    return dt


@st.cache
def get_region_pred_data():
    dt = main_db.get_df_from_mysql('预测房屋价格变化趋势')
    return dt


@st.cache
def get_all_pred_data():
    dt = main_db.get_df_from_mysql('预测房屋价格')
    return dt


@st.cache
def get_all_data():
    dt = main_db.get_df_from_mysql('数据')
    return dt


all_data_df = get_data()
all_pred_df = get_all_pred_data()
region_pred_df = get_region_pred_data()
adminc = list(set(region_pred_df['行政区']))
# data = get_data()

# @st.cache(allow_output_mutation=True)
# def get_houseDf():
#     df = main_db.get_house_df()
#     return df


house_df = main_db.get_house_df()
new_df = main_db.get_house_region_df()
all_pred = main_db.all_pred(house_df)
cities = list(set(house_df['region']))


def show_data(ct):
    if len(ct) > 1:
        ct1 = ct[0][0:2]
        ct2 = ct[1][0:2]
        df_ct1 = all_pred_df[all_pred_df['region'] == ct1]
        df_ct1.sort_values(by="预测价格(w)", inplace=True, ascending=True)
        ids1 = df_ct1['False'][0:5].to_list()
        df_ct2 = all_pred_df[all_pred_df['region'] == ct2]
        df_ct2.sort_values(by="预测价格(w)", inplace=True, ascending=True)
        ids2 = df_ct2['False'][0:5].to_list()
        ids = ids1 + ids2
    else:
        df_ct = all_pred_df[all_pred_df['region'] == ct[0][0:2]]
        df_ct.sort_values(by="预测价格(w)", inplace=True, ascending=True)
        ids = df_ct['False'][0:5].to_list()
    res = all_data_df[all_data_df['False'].isin(ids)]
    org_df = all_pred_df[all_pred_df['False'].isin(ids)][['False', '预测价格(w)']]
    res = pd.merge(res, org_df, how='inner', on='False')
    return res


def fig_line(ct):
    matplotlib.rc("font", family='Heiti TC')
    pds = region_pred_df[region_pred_df['行政区'].isin(ct)]
    fig = plt.figure(figsize=(10, 6))
    cs = ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
    if len(ct) > 1:
        ct1 = ct[0]
        ct2 = ct[1]
        pds1 = pds[pds['行政区'] == ct1]
        pds2 = pds[pds['行政区'] == ct2]
        pds1_df = pds1[cs]
        pds2_df = pds2[cs]
        y1 = pds1_df.values[0]
        x1 = range(1, 13)
        x2 = range(1, 13)
        y2 = pds2_df.values[0]
        plt.plot(x1, y1, label=ct1, linewidth=3, color='r', marker='o',
                 markerfacecolor='blue', markersize=12)
        plt.plot(x2, y2, label=ct2, linewidth=3, color='y', marker='o',
                 markerfacecolor='blue', markersize=12)
    else:
        pds_df = pds[cs]
        y1 = pds_df.values[0]
        x1 = range(1, 13)
        plt.plot(x1, y1, label=ct[0], linewidth=3, color='r', marker='o',
                 markerfacecolor='blue', markersize=12)
    plt.xlabel('月份')
    plt.ylabel('房价')
    plt.title('预测房屋价格变化趋势')
    plt.legend()
    return fig


def get_fig_df(cts):
    if cts is None or len(cts) <= 1:
        if len(cts) == 1:
            return house_df[house_df['region'] == cts[0][0:2]]
        else:
            return house_df
    else:
        return new_df[new_df['行政区'].isin(cts)]


def fig_single_x_analysis(ct):
    matplotlib.rc("font", family='Heiti TC')
    fig = plt.figure(figsize=(15, 15))
    if len(ct) <= 1:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['city', 'region'])
        for i in range(1, 7):
            ax = plt.subplot(3, 3, i)
            length = 1000
            idx = np.random.permutation(np.arange(hou_df.shape[0]))[:length]
            x = hou_df.iloc[:, i - 1].to_numpy()[idx]
            y = hou_df['总价(w)'].to_numpy()[idx]
            ax.scatter(x, np.log(y))
            ax.set_xlabel(hou_df.columns[i - 1])
            ax.set_ylabel('log(price)')
    else:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['城市', '行政区'])
        for i in range(0, 6):
            ax = plt.subplot(2, 3, i + 1)
            x = hou_df.iloc[:, i].to_numpy()
            y = hou_df['4'].to_numpy()
            ax.scatter(x, y)
            ax.set_xlabel(hou_df.columns[i])
            ax.set_ylabel('房价均价')
    return fig


def fig_corr(ct):
    matplotlib.rc("font", family='Heiti TC')
    if len(ct) <= 1:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['city', 'region'])
    else:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['城市', '行政区'])
    corr = hou_df.corr()
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(corr, annot=True, cbar_kws={'label': 'heatmap'}, ax=ax)
    return fig


def fig_multi_x_analysis(ct):
    if len(ct) <= 1:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['city', 'region'])
        cols = ['面积', '满五/满二', '优质教育', '地铁', '地区均价(k/m2)', '区域均价(k/m2)']
        t = '总价(w)'
    else:
        hou_df = get_fig_df(ct)
        hou_df = hou_df.drop(columns=['城市', '行政区'])
        cols = ['城市级别', 'GDP', '空气质量综合指数', '1', '2', '3']
        t = '4'

    def looper(df, limit):
        try:
            for i in range(len(cols)):
                data1 = df[cols]
                x = sm.add_constant(data1)  # 生成自变量
                y = df[t]  # 生成因变量
                model = sm.OLS(y, x)  # 生成模型
                resul = model.fit()  # 模型拟合
                p_values = resul.pvalues  # 得到结果中所有P值
                p_values.drop('const', inplace=True)  # 把const取得
                p_max = max(p_values)  # 选出最大的P值
                if p_max > limit:
                    ind = p_values.idxmax()  # 找出最大P值的index
                    cols.remove(ind)  # 把这个index从cols中删除
                else:
                    return resul
        except:
            return None

    res = looper(hou_df, 0.05)

    if res is None:
        return '数据缺失！'
    else:
        return res.summary()


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


menu = ['房价数据展示', '房价数据分析', '房价数据预测', '房价数据导入', '房价预测数据导出']
# if 'count' not in st.session_state:
#     st.session_state.count = 0

choice = st.sidebar.radio("福建房价数据可视化分析与预测", menu)
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
if choice == '房价数据分析':
    st.title('房价数据分析 ☕ ')
    city = st.multiselect('', tuple(adminc))
    if len(city) == 0:
        st.header('全量数据分析')
    else:
        st.header('区域数据分析')
    st.subheader('单因素分析图')
    st.pyplot(fig_single_x_analysis(city))
    st.subheader('相关系数的热力图')
    st.pyplot(fig_corr(city))
    st.subheader('多因素分析结果表')
    st.write(fig_multi_x_analysis(city))
elif choice == '房价数据预测':
    st.title('房价数据预测')
    city = st.multiselect('', tuple(adminc))
    if city:
        st.subheader('房价预测趋势图')
        st.pyplot(fig_line(city))
        st.subheader('房价预测信息')
        result = show_data(city)
        st.dataframe(result)
elif choice == '房价数据导入':
    st.title('房价数据导入')
    uploaded_file = st.file_uploader('上传一份文件')
    if uploaded_file is not None:
        updt = None
        if 'csv' in uploaded_file.name:
            updt = pd.read_csv(uploaded_file)
        elif 'xls' in uploaded_file.name:
            updt = pd.read_excel(uploaded_file)
        if updt is not None:
            st.dataframe(updt)
            main_db.dt_mysql(updt, 'shuju')
            st.success('上传文件成功')
            st.balloons()
elif choice == '房价预测数据导出':
    st.title('房价预测数据导出')
    city = st.multiselect('', tuple(adminc))
    if city:
        choice_df = show_data(city)
        st.dataframe(choice_df)
        csv = convert_df(choice_df)
        st.download_button(
            label="以CSV格式下载",
            data=csv,
            file_name='{0}.csv'.format(city),
            mime='text/csv'
        )

elif choice == '房价数据展示':
    st.title('房价数据展示 ☕ ')
    tables = ['福建房价', '福建各市空气质量指数', '福建各市GDP', '漳州空气质量指数']
    table = st.selectbox('选择一个数据', tables)
    if table == '福建房价':
        components.html("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>基于Pyecharts的可视化大屏</title>
            <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/fujian.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/themes/macarons.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/ResizeSensor.js"></script>

            <link rel="stylesheet"  href="https://assets.pyecharts.org/assets/jquery-ui.css">

</head>
<body>
    <style>.box {  }; </style>
        
    <div class="box">
                <div id="973a5bb8ebcd4146acd823aaa5c6395b" class="chart-container" style="position: absolute; width: 959px; height: 722px; top: 43px; left: 754px;"></div>
    <script>
        var chart_973a5bb8ebcd4146acd823aaa5c6395b = echarts.init(
            document.getElementById('973a5bb8ebcd4146acd823aaa5c6395b'), 'white', {renderer: 'canvas'});
        var option_973a5bb8ebcd4146acd823aaa5c6395b = {
    "baseOption": {
        "series": [
            {
                "type": "map",
                "name": "\u5e73\u5747\u623f\u4ef7",
                "label": {
                    "show": true,
                    "position": "top",
                    "margin": 8
                },
                "mapType": "\u798f\u5efa",
                "data": [
                    {
                        "name": "\u798f\u5dde\u5e02",
                        "value": 16508.70513
                    },
                    {
                        "name": "\u53a6\u95e8\u5e02",
                        "value": 38161.16667
                    },
                    {
                        "name": "\u4e09\u660e\u5e02",
                        "value": 8859.666667
                    },
                    {
                        "name": "\u6cc9\u5dde\u5e02",
                        "value": 13029.39583
                    },
                    {
                        "name": "\u6f33\u5dde\u5e02",
                        "value": 9120.522727
                    },
                    {
                        "name": "\u5357\u5e73\u5e02",
                        "value": 8119.770833
                    },
                    {
                        "name": "\u9f99\u5ca9\u5e02",
                        "value": 10076.85714
                    },
                    {
                        "name": "\u5b81\u5fb7\u5e02",
                        "value": 10607.7381
                    }
                ],
                "roam": true,
                "aspectScale": 0.75,
                "nameProperty": "name",
                "selectedMode": false,
                "zoom": 1,
                "mapValueCalculation": "sum",
                "showLegendSymbol": true,
                "emphasis": {}
            }
        ],
        "timeline": {
            "axisType": "category",
            "orient": "horizontal",
            "autoPlay": false,
            "controlPosition": "left",
            "loop": true,
            "rewind": false,
            "show": true,
            "inverse": false,
            "bottom": "-5px",
            "data": [
                "2019\u5e74",
                "2020\u5e74",
                "2021\u5e74"
            ]
        },
        "visualMap": {
            "show": true,
            "type": "continuous",
            "min": 0,
            "max": 40000,
            "inRange": {
                "color": [
                    "#50a3ba",
                    "#eac763",
                    "#d94e5d"
                ]
            },
            "calculable": true,
            "inverse": false,
            "splitNumber": 5,
            "orient": "vertical",
            "showLabel": true,
            "itemWidth": 20,
            "itemHeight": 140,
            "borderWidth": 0
        }
    },
    "options": [
        {
            "legend": [
                {
                    "data": [
                        "\u5e73\u5747\u623f\u4ef7"
                    ],
                    "selected": {
                        "\u5e73\u5747\u623f\u4ef7": true
                    },
                    "show": true,
                    "padding": 5,
                    "itemGap": 10,
                    "itemWidth": 25,
                    "itemHeight": 14
                }
            ],
            "series": [
                {
                    "type": "map",
                    "name": "\u5e73\u5747\u623f\u4ef7",
                    "label": {
                        "show": true,
                        "position": "top",
                        "margin": 8
                    },
                    "mapType": "\u798f\u5efa",
                    "data": [
                        {
                            "name": "\u798f\u5dde\u5e02",
                            "value": 16946.7948717949
                        },
                        {
                            "name": "\u53a6\u95e8\u5e02",
                            "value": 33619.63889
                        },
                        {
                            "name": "\u4e09\u660e\u5e02",
                            "value": 8522.398148
                        },
                        {
                            "name": "\u6cc9\u5dde\u5e02",
                            "value": 9984.979167
                        },
                        {
                            "name": "\u6f33\u5dde\u5e02",
                            "value": 8702.537879
                        },
                        {
                            "name": "\u5357\u5e73\u5e02",
                            "value": 7886.364583
                        },
                        {
                            "name": "\u9f99\u5ca9\u5e02",
                            "value": 9434.84523
                        },
                        {
                            "name": "\u5b81\u5fb7\u5e02",
                            "value": 10273.86905
                        }
                    ],
                    "roam": true,
                    "aspectScale": 0.75,
                    "nameProperty": "name",
                    "selectedMode": false,
                    "zoom": 1,
                    "mapValueCalculation": "sum",
                    "showLegendSymbol": true,
                    "emphasis": {}
                }
            ],
            "title": [
                {
                    "text": "\u798f\u5efa2019\u5e74\u623f\u4ef7\u6570\u636e",
                    "padding": 5,
                    "itemGap": 10
                }
            ],
            "tooltip": {
                "show": true,
                "trigger": "item",
                "triggerOn": "mousemove|click",
                "axisPointer": {
                    "type": "line"
                },
                "showContent": true,
                "alwaysShowContent": false,
                "showDelay": 0,
                "hideDelay": 100,
                "textStyle": {
                    "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5
            },
            "visualMap": {
                "show": true,
                "type": "continuous",
                "min": 0,
                "max": 40000,
                "inRange": {
                    "color": [
                        "#50a3ba",
                        "#eac763",
                        "#d94e5d"
                    ]
                },
                "calculable": true,
                "inverse": false,
                "splitNumber": 5,
                "orient": "vertical",
                "showLabel": true,
                "itemWidth": 20,
                "itemHeight": 140,
                "borderWidth": 0
            },
            "color": [
                "#c23531",
                "#2f4554",
                "#61a0a8",
                "#d48265",
                "#749f83",
                "#ca8622",
                "#bda29a",
                "#6e7074",
                "#546570",
                "#c4ccd3",
                "#f05b72",
                "#ef5b9c",
                "#f47920",
                "#905a3d",
                "#fab27b",
                "#2a5caa",
                "#444693",
                "#726930",
                "#b2d235",
                "#6d8346",
                "#ac6767",
                "#1d953f",
                "#6950a1",
                "#918597"
            ]
        },
        {
            "legend": [
                {
                    "data": [
                        "\u5e73\u5747\u623f\u4ef7"
                    ],
                    "selected": {
                        "\u5e73\u5747\u623f\u4ef7": true
                    },
                    "show": true,
                    "padding": 5,
                    "itemGap": 10,
                    "itemWidth": 25,
                    "itemHeight": 14
                }
            ],
            "series": [
                {
                    "type": "map",
                    "name": "\u5e73\u5747\u623f\u4ef7",
                    "label": {
                        "show": true,
                        "position": "top",
                        "margin": 8
                    },
                    "mapType": "\u798f\u5efa",
                    "data": [
                        {
                            "name": "\u798f\u5dde\u5e02",
                            "value": 16457.69872
                        },
                        {
                            "name": "\u53a6\u95e8\u5e02",
                            "value": 34846.11111
                        },
                        {
                            "name": "\u4e09\u660e\u5e02",
                            "value": 9098.935185
                        },
                        {
                            "name": "\u6cc9\u5dde\u5e02",
                            "value": 10748.91667
                        },
                        {
                            "name": "\u6f33\u5dde\u5e02",
                            "value": 8979.310606
                        },
                        {
                            "name": "\u5357\u5e73\u5e02",
                            "value": 8056.802083
                        },
                        {
                            "name": "\u9f99\u5ca9\u5e02",
                            "value": 9690.119048
                        },
                        {
                            "name": "\u5b81\u5fb7\u5e02",
                            "value": 10775.47619
                        }
                    ],
                    "roam": true,
                    "aspectScale": 0.75,
                    "nameProperty": "name",
                    "selectedMode": false,
                    "zoom": 1,
                    "mapValueCalculation": "sum",
                    "showLegendSymbol": true,
                    "emphasis": {}
                }
            ],
            "title": [
                {
                    "text": "\u798f\u5efa2020\u5e74\u623f\u4ef7\u6570\u636e",
                    "padding": 5,
                    "itemGap": 10
                }
            ],
            "tooltip": {
                "show": true,
                "trigger": "item",
                "triggerOn": "mousemove|click",
                "axisPointer": {
                    "type": "line"
                },
                "showContent": true,
                "alwaysShowContent": false,
                "showDelay": 0,
                "hideDelay": 100,
                "textStyle": {
                    "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5
            },
            "visualMap": {
                "show": true,
                "type": "continuous",
                "min": 0,
                "max": 40000,
                "inRange": {
                    "color": [
                        "#50a3ba",
                        "#eac763",
                        "#d94e5d"
                    ]
                },
                "calculable": true,
                "inverse": false,
                "splitNumber": 5,
                "orient": "vertical",
                "showLabel": true,
                "itemWidth": 20,
                "itemHeight": 140,
                "borderWidth": 0
            },
            "color": [
                "#c23531",
                "#2f4554",
                "#61a0a8",
                "#d48265",
                "#749f83",
                "#ca8622",
                "#bda29a",
                "#6e7074",
                "#546570",
                "#c4ccd3",
                "#f05b72",
                "#ef5b9c",
                "#f47920",
                "#905a3d",
                "#fab27b",
                "#2a5caa",
                "#444693",
                "#726930",
                "#b2d235",
                "#6d8346",
                "#ac6767",
                "#1d953f",
                "#6950a1",
                "#918597"
            ]
        },
        {
            "legend": [
                {
                    "data": [
                        "\u5e73\u5747\u623f\u4ef7"
                    ],
                    "selected": {
                        "\u5e73\u5747\u623f\u4ef7": true
                    },
                    "show": true,
                    "padding": 5,
                    "itemGap": 10,
                    "itemWidth": 25,
                    "itemHeight": 14
                }
            ],
            "series": [
                {
                    "type": "map",
                    "name": "\u5e73\u5747\u623f\u4ef7",
                    "label": {
                        "show": true,
                        "position": "top",
                        "margin": 8
                    },
                    "mapType": "\u798f\u5efa",
                    "data": [
                        {
                            "name": "\u798f\u5dde\u5e02",
                            "value": 16508.70513
                        },
                        {
                            "name": "\u53a6\u95e8\u5e02",
                            "value": 38161.16667
                        },
                        {
                            "name": "\u4e09\u660e\u5e02",
                            "value": 8859.666667
                        },
                        {
                            "name": "\u6cc9\u5dde\u5e02",
                            "value": 13029.39583
                        },
                        {
                            "name": "\u6f33\u5dde\u5e02",
                            "value": 9120.522727
                        },
                        {
                            "name": "\u5357\u5e73\u5e02",
                            "value": 8119.770833
                        },
                        {
                            "name": "\u9f99\u5ca9\u5e02",
                            "value": 10076.85714
                        },
                        {
                            "name": "\u5b81\u5fb7\u5e02",
                            "value": 10607.7381
                        }
                    ],
                    "roam": true,
                    "aspectScale": 0.75,
                    "nameProperty": "name",
                    "selectedMode": false,
                    "zoom": 1,
                    "mapValueCalculation": "sum",
                    "showLegendSymbol": true,
                    "emphasis": {}
                }
            ],
            "title": [
                {
                    "text": "\u798f\u5efa2021\u5e74\u623f\u4ef7\u6570\u636e",
                    "padding": 5,
                    "itemGap": 10
                }
            ],
            "tooltip": {
                "show": true,
                "trigger": "item",
                "triggerOn": "mousemove|click",
                "axisPointer": {
                    "type": "line"
                },
                "showContent": true,
                "alwaysShowContent": false,
                "showDelay": 0,
                "hideDelay": 100,
                "textStyle": {
                    "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5
            },
            "visualMap": {
                "show": true,
                "type": "continuous",
                "min": 0,
                "max": 40000,
                "inRange": {
                    "color": [
                        "#50a3ba",
                        "#eac763",
                        "#d94e5d"
                    ]
                },
                "calculable": true,
                "inverse": false,
                "splitNumber": 5,
                "orient": "vertical",
                "showLabel": true,
                "itemWidth": 20,
                "itemHeight": 140,
                "borderWidth": 0
            },
            "color": [
                "#c23531",
                "#2f4554",
                "#61a0a8",
                "#d48265",
                "#749f83",
                "#ca8622",
                "#bda29a",
                "#6e7074",
                "#546570",
                "#c4ccd3",
                "#f05b72",
                "#ef5b9c",
                "#f47920",
                "#905a3d",
                "#fab27b",
                "#2a5caa",
                "#444693",
                "#726930",
                "#b2d235",
                "#6d8346",
                "#ac6767",
                "#1d953f",
                "#6950a1",
                "#918597"
            ]
        }
    ]
};
        chart_973a5bb8ebcd4146acd823aaa5c6395b.setOption(option_973a5bb8ebcd4146acd823aaa5c6395b);
    </script>
<br/>                        <style>
            .fl-table {
                margin: 20px;
                border-radius: 5px;
                font-size: 12px;
                border: none;
                border-collapse: collapse;
                max-width: 100%;
                white-space: nowrap;
                word-break: keep-all;
            }

            .fl-table th {
                text-align: left;
                font-size: 20px;
            }

            .fl-table tr {
                display: table-row;
                vertical-align: inherit;
                border-color: inherit;
            }

            .fl-table tr:hover td {
                background: #00d1b2;
                color: #F8F8F8;
            }

            .fl-table td, .fl-table th {
                border-style: none;
                border-top: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-bottom: 3px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                padding: .5em .55em;
                font-size: 15px;
            }

            .fl-table td {
                border-style: none;
                font-size: 15px;
                vertical-align: center;
                border-bottom: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                height: 30px;
            }

            .fl-table tr:nth-child(even) {
                background: #F8F8F8;
            }
        </style>
        <div id="01625341b5054e848aedd39fd78c8a25" class="chart-container" style="position: absolute; width: 561px; height: 722px; top: 42px; left: 152px;">
            <p class="title" style="font-size: 18px; font-weight:bold;" > 福建房价数据</p>
            <p class="subtitle" style="font-size: 12px;" > 2019-2021年房价</p>
            <table class="fl-table">
    <thead>
        <tr>
            <th>地区</th>
            <th>2021</th>
            <th>2020</th>
            <th>2019</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>福州市</td>
            <td>16508.70513</td>
            <td>16457.69872</td>
            <td>16946.79487</td>
        </tr>
        <tr>
            <td>厦门市</td>
            <td>38161.16667</td>
            <td>34846.11111</td>
            <td>33619.63889</td>
        </tr>
        <tr>
            <td>三明市</td>
            <td>8859.666667</td>
            <td>9098.935185</td>
            <td>8522.398148</td>
        </tr>
        <tr>
            <td>泉州市</td>
            <td>13029.39583</td>
            <td>10748.91667</td>
            <td>9984.979167</td>
        </tr>
        <tr>
            <td>漳州市</td>
            <td>9120.522727</td>
            <td>8979.310606</td>
            <td>8702.537879</td>
        </tr>
        <tr>
            <td>南平市</td>
            <td>8119.770833</td>
            <td>8056.802083</td>
            <td>7886.364583</td>
        </tr>
        <tr>
            <td>龙岩市</td>
            <td>10076.85714</td>
            <td>9690.119048</td>
            <td>9434.845238</td>
        </tr>
        <tr>
            <td>宁德市</td>
            <td>10607.7381</td>
            <td>10775.47619</td>
            <td>10273.86905</td>
        </tr>
    </tbody>
</table>
        </div>

<br/>                <div id="e7c3dcac153f45adb607e81e2e0db506" class="chart-container" style="position: absolute; width: 1560px; height: 598px; top: 791px; left: 155px;"></div>
    <script>
        var chart_e7c3dcac153f45adb607e81e2e0db506 = echarts.init(
            document.getElementById('e7c3dcac153f45adb607e81e2e0db506'), 'macarons', {renderer: 'canvas'});
        var option_e7c3dcac153f45adb607e81e2e0db506 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "series": [
        {
            "type": "bar",
            "name": "2019",
            "legendHoverLink": true,
            "data": [
                16946.7948717949,
                33619.6388888889,
                8522.39814814815,
                9984.97916666667,
                8702.53787878788,
                7886.36458333333,
                9434.84523809524,
                10273.869047619
            ],
            "showBackground": false,
            "barMinHeight": 0,
            "barCategoryGap": "20%",
            "barGap": "30%",
            "large": false,
            "largeThreshold": 400,
            "seriesLayoutBy": "column",
            "datasetIndex": 0,
            "clip": true,
            "zlevel": 0,
            "z": 2,
            "label": {
                "show": true,
                "position": "top",
                "margin": 8
            }
        },
        {
            "type": "bar",
            "name": "2020",
            "legendHoverLink": true,
            "data": [
                16457.69872,
                34846.11111,
                9098.935185,
                10748.91667,
                8979.310606,
                8056.802083,
                9690.119048,
                10775.47619
            ],
            "showBackground": false,
            "barMinHeight": 0,
            "barCategoryGap": "20%",
            "barGap": "30%",
            "large": false,
            "largeThreshold": 400,
            "seriesLayoutBy": "column",
            "datasetIndex": 0,
            "clip": true,
            "zlevel": 0,
            "z": 2,
            "label": {
                "show": true,
                "position": "top",
                "margin": 8
            }
        },
        {
            "type": "bar",
            "name": "2021",
            "legendHoverLink": true,
            "data": [
                16508.70513,
                38161.16667,
                8859.666667,
                13029.39583,
                9120.522727,
                8119.770833,
                10076.85714,
                10607.7381
            ],
            "showBackground": false,
            "barMinHeight": 0,
            "barCategoryGap": "20%",
            "barGap": "30%",
            "large": false,
            "largeThreshold": 400,
            "seriesLayoutBy": "column",
            "datasetIndex": 0,
            "clip": true,
            "zlevel": 0,
            "z": 2,
            "label": {
                "show": true,
                "position": "top",
                "margin": 8
            }
        }
    ],
    "legend": [
        {
            "data": [
                "2019",
                "2020",
                "2021"
            ],
            "selected": {
                "2019": true,
                "2020": true,
                "2021": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "xAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": false,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            },
            "data": [
                "\u798f\u5dde\u5e02",
                "\u53a6\u95e8\u5e02",
                "\u4e09\u660e\u5e02",
                "\u6cc9\u5dde\u5e02",
                "\u6f33\u5dde\u5e02",
                "\u5357\u5e73\u5e02",
                "\u9f99\u5ca9\u5e02",
                "\u5b81\u5fb7\u5e02"
            ]
        }
    ],
    "yAxis": [
        {
            "show": true,
            "scale": false,
            "nameLocation": "end",
            "nameGap": 15,
            "gridIndex": 0,
            "inverse": false,
            "offset": 0,
            "splitNumber": 5,
            "minInterval": 0,
            "splitLine": {
                "show": false,
                "lineStyle": {
                    "show": true,
                    "width": 1,
                    "opacity": 1,
                    "curveness": 0,
                    "type": "solid"
                }
            }
        }
    ],
    "title": {
        "text": "\u798f\u5efa\u623f\u4ef7\u6570\u636e-\u67f1\u72b6\u56fe",
        "subtext": "2019-2021\u5e74\u623f\u4ef7"
    }
};
        chart_e7c3dcac153f45adb607e81e2e0db506.setOption(option_e7c3dcac153f45adb607e81e2e0db506);
    </script>
<br/>    </div>
    <script>
            $('#973a5bb8ebcd4146acd823aaa5c6395b').css('border-style', 'dashed').css('border-width', '0px');$("#973a5bb8ebcd4146acd823aaa5c6395b>div:nth-child(1)").width("100%").height("100%");
            new ResizeSensor(jQuery('#973a5bb8ebcd4146acd823aaa5c6395b'), function() { chart_973a5bb8ebcd4146acd823aaa5c6395b.resize()});
            $('#01625341b5054e848aedd39fd78c8a25').css('border-style', 'dashed').css('border-width', '0px');$("#01625341b5054e848aedd39fd78c8a25>div:nth-child(1)").width("100%").height("100%");
            $('#e7c3dcac153f45adb607e81e2e0db506').css('border-style', 'dashed').css('border-width', '0px');$("#e7c3dcac153f45adb607e81e2e0db506>div:nth-child(1)").width("100%").height("100%");
            new ResizeSensor(jQuery('#e7c3dcac153f45adb607e81e2e0db506'), function() { chart_e7c3dcac153f45adb607e81e2e0db506.resize()});
            var charts_id = ['973a5bb8ebcd4146acd823aaa5c6395b','01625341b5054e848aedd39fd78c8a25','e7c3dcac153f45adb607e81e2e0db506'];
function downloadCfg () {
    const fileName = 'chart_config.json'
    let downLink = document.createElement('a')
    downLink.download = fileName

    let result = []
    for(let i=0; i<charts_id.length; i++) {
        chart = $('#'+charts_id[i])
        result.push({
            cid: charts_id[i],
            width: chart.css("width"),
            height: chart.css("height"),
            top: chart.offset().top + "px",
            left: chart.offset().left + "px"
        })
    }

    let blob = new Blob([JSON.stringify(result)])
    downLink.href = URL.createObjectURL(blob)
    document.body.appendChild(downLink)
    downLink.click()
    document.body.removeChild(downLink)
}
    </script>
</body>
</html>
""",
                        height=1300,
                        width=1500
                        )
    elif table == '福建各市空气质量指数':
        components.html("""
        <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>基于Pyecharts的可视化大屏</title>
            <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/fujian.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/ResizeSensor.js"></script>

            <link rel="stylesheet"  href="https://assets.pyecharts.org/assets/jquery-ui.css">

</head>
<body>
    <style>.box {  }; </style>
        
    <div class="box">
                        <style>
            .fl-table {
                margin: 20px;
                border-radius: 5px;
                font-size: 12px;
                border: none;
                border-collapse: collapse;
                max-width: 100%;
                white-space: nowrap;
                word-break: keep-all;
            }

            .fl-table th {
                text-align: left;
                font-size: 20px;
            }

            .fl-table tr {
                display: table-row;
                vertical-align: inherit;
                border-color: inherit;
            }

            .fl-table tr:hover td {
                background: #00d1b2;
                color: #F8F8F8;
            }

            .fl-table td, .fl-table th {
                border-style: none;
                border-top: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-bottom: 3px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                padding: .5em .55em;
                font-size: 15px;
            }

            .fl-table td {
                border-style: none;
                font-size: 15px;
                vertical-align: center;
                border-bottom: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                height: 30px;
            }

            .fl-table tr:nth-child(even) {
                background: #F8F8F8;
            }
        </style>
        <div id="b0932317ed374774b6895f95a3ef77ee" class="chart-container" style="position: absolute; width: 304px; height: 922px; top: 42px; left: 112px;">
            <p class="title" style="font-size: 18px; font-weight:bold;" > 福建空气指数数据</p>
            <p class="subtitle" style="font-size: 12px;" > </p>
            <table class="fl-table">
    <thead>
        <tr>
            <th>地区</th>
            <th>空气指数</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>福州市</td>
            <td>2.360833333</td>
        </tr>
        <tr>
            <td>厦门市</td>
            <td>2.21333333333333</td>
        </tr>
        <tr>
            <td>三明市</td>
            <td>2.025</td>
        </tr>
        <tr>
            <td>泉州市</td>
            <td>2.45307692307692</td>
        </tr>
        <tr>
            <td>漳州市</td>
            <td>2.543125</td>
        </tr>
        <tr>
            <td>南平市</td>
            <td>2.157</td>
        </tr>
        <tr>
            <td>龙岩市</td>
            <td>2.18428571428571</td>
        </tr>
        <tr>
            <td>宁德市</td>
            <td>2.1</td>
        </tr>
    </tbody>
</table>
        </div>

<br/>                <div id="de60d7055f6f47ffa8792f82b6ba621a" class="chart-container" style="position: absolute; width: 900px; height: 796px; top: 45px; left: 446px;"></div>
    <script>
        var chart_de60d7055f6f47ffa8792f82b6ba621a = echarts.init(
            document.getElementById('de60d7055f6f47ffa8792f82b6ba621a'), 'white', {renderer: 'canvas'});
        var option_de60d7055f6f47ffa8792f82b6ba621a = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597"
    ],
    "series": [
        {
            "type": "map",
            "name": "\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570",
            "label": {
                "show": true,
                "position": "top",
                "color": "blue",
                "margin": 8
            },
            "mapType": "\u798f\u5efa",
            "data": [
                {
                    "name": "\u798f\u5dde\u5e02",
                    "value": 2.360833333
                },
                {
                    "name": "\u53a6\u95e8\u5e02",
                    "value": 2.21333333333333
                },
                {
                    "name": "\u4e09\u660e\u5e02",
                    "value": 2.025
                },
                {
                    "name": "\u6cc9\u5dde\u5e02",
                    "value": 2.45307692307692
                },
                {
                    "name": "\u6f33\u5dde\u5e02",
                    "value": 2.543125
                },
                {
                    "name": "\u5357\u5e73\u5e02",
                    "value": 2.157
                },
                {
                    "name": "\u9f99\u5ca9\u5e02",
                    "value": 2.18428571428571
                },
                {
                    "name": "\u5b81\u5fb7\u5e02",
                    "value": 2.1
                }
            ],
            "roam": true,
            "aspectScale": 0.75,
            "nameProperty": "name",
            "selectedMode": false,
            "zoom": 1,
            "mapValueCalculation": "sum",
            "showLegendSymbol": true,
            "emphasis": {},
            "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
            }
        }
    ],
    "legend": [
        {
            "data": [
                "\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570"
            ],
            "selected": {
                "\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "title": [
        {
            "text": "\u798f\u5efa\u7701\u5730\u56fe",
            "padding": 5,
            "itemGap": 10
        }
    ],
    "visualMap": {
        "show": true,
        "type": "continuous",
        "min": 2.0,
        "max": 2.6,
        "inRange": {
            "color": [
                "#50a3ba",
                "#eac763",
                "#d94e5d"
            ]
        },
        "calculable": true,
        "inverse": false,
        "splitNumber": 5,
        "orient": "vertical",
        "showLabel": true,
        "itemWidth": 20,
        "itemHeight": 140,
        "borderWidth": 0
    }
};
        chart_de60d7055f6f47ffa8792f82b6ba621a.setOption(option_de60d7055f6f47ffa8792f82b6ba621a);
    </script>
<br/>    </div>
    <script>
            $('#b0932317ed374774b6895f95a3ef77ee').css('border-style', 'dashed').css('border-width', '0px');$("#b0932317ed374774b6895f95a3ef77ee>div:nth-child(1)").width("100%").height("100%");
            $('#de60d7055f6f47ffa8792f82b6ba621a').css('border-style', 'dashed').css('border-width', '0px');$("#de60d7055f6f47ffa8792f82b6ba621a>div:nth-child(1)").width("100%").height("100%");
            new ResizeSensor(jQuery('#de60d7055f6f47ffa8792f82b6ba621a'), function() { chart_de60d7055f6f47ffa8792f82b6ba621a.resize()});
            var charts_id = ['b0932317ed374774b6895f95a3ef77ee','de60d7055f6f47ffa8792f82b6ba621a'];
function downloadCfg () {
    const fileName = 'chart_config.json'
    let downLink = document.createElement('a')
    downLink.download = fileName

    let result = []
    for(let i=0; i<charts_id.length; i++) {
        chart = $('#'+charts_id[i])
        result.push({
            cid: charts_id[i],
            width: chart.css("width"),
            height: chart.css("height"),
            top: chart.offset().top + "px",
            left: chart.offset().left + "px"
        })
    }

    let blob = new Blob([JSON.stringify(result)])
    downLink.href = URL.createObjectURL(blob)
    document.body.appendChild(downLink)
    downLink.click()
    document.body.removeChild(downLink)
}
    </script>
</body>
</html>
 """,
                        height=800,
                        width=1500
                        )
    elif table == '福建各市GDP':
        components.html("""
        <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>基于Pyecharts的可视化大屏</title>
            <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/fujian.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/ResizeSensor.js"></script>

            <link rel="stylesheet"  href="https://assets.pyecharts.org/assets/jquery-ui.css">

</head>
<body>
    <style>.box {  }; </style>
        
    <div class="box">
                <div id="26119098d0fe4817b054ffff4e2317b3" class="chart-container" style="position: absolute; width: 900px; height: 804px; top: 39px; left: 627px;"></div>
    <script>
        var chart_26119098d0fe4817b054ffff4e2317b3 = echarts.init(
            document.getElementById('26119098d0fe4817b054ffff4e2317b3'), 'white', {renderer: 'canvas'});
        var option_26119098d0fe4817b054ffff4e2317b3 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597"
    ],
    "series": [
        {
            "type": "map",
            "name": "GDP",
            "label": {
                "show": true,
                "position": "top",
                "color": "blue",
                "margin": 8
            },
            "mapType": "\u798f\u5efa",
            "data": [
                {
                    "name": "\u798f\u5dde\u5e02",
                    "value": 11324.48
                },
                {
                    "name": "\u53a6\u95e8\u5e02",
                    "value": 7033.89
                },
                {
                    "name": "\u4e09\u660e\u5e02",
                    "value": 2702.19
                },
                {
                    "name": "\u6cc9\u5dde\u5e02",
                    "value": 10376.76
                },
                {
                    "name": "\u6f33\u5dde\u5e02",
                    "value": 5025.4
                },
                {
                    "name": "\u5357\u5e73\u5e02",
                    "value": 2007.4
                },
                {
                    "name": "\u9f99\u5ca9\u5e02",
                    "value": 3081.78
                },
                {
                    "name": "\u5b81\u5fb7\u5e02",
                    "value": 3151.08
                }
            ],
            "roam": true,
            "aspectScale": 0.75,
            "nameProperty": "name",
            "selectedMode": false,
            "zoom": 1,
            "mapValueCalculation": "sum",
            "showLegendSymbol": true,
            "emphasis": {},
            "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
            }
        }
    ],
    "legend": [
        {
            "data": [
                "GDP"
            ],
            "selected": {
                "GDP": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "title": [
        {
            "text": "\u798f\u5efa\u7701\u5730\u56fe",
            "padding": 5,
            "itemGap": 10
        }
    ],
    "visualMap": {
        "show": true,
        "type": "continuous",
        "min": 0,
        "max": 12000,
        "inRange": {
            "color": [
                "#50a3ba",
                "#eac763",
                "#d94e5d"
            ]
        },
        "calculable": true,
        "inverse": false,
        "splitNumber": 5,
        "orient": "vertical",
        "showLabel": true,
        "itemWidth": 20,
        "itemHeight": 140,
        "borderWidth": 0
    }
};
        chart_26119098d0fe4817b054ffff4e2317b3.setOption(option_26119098d0fe4817b054ffff4e2317b3);
    </script>
<br/>                        <style>
            .fl-table {
                margin: 20px;
                border-radius: 5px;
                font-size: 12px;
                border: none;
                border-collapse: collapse;
                max-width: 100%;
                white-space: nowrap;
                word-break: keep-all;
            }

            .fl-table th {
                text-align: left;
                font-size: 20px;
            }

            .fl-table tr {
                display: table-row;
                vertical-align: inherit;
                border-color: inherit;
            }

            .fl-table tr:hover td {
                background: #00d1b2;
                color: #F8F8F8;
            }

            .fl-table td, .fl-table th {
                border-style: none;
                border-top: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-bottom: 3px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                padding: .5em .55em;
                font-size: 15px;
            }

            .fl-table td {
                border-style: none;
                font-size: 15px;
                vertical-align: center;
                border-bottom: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                height: 30px;
            }

            .fl-table tr:nth-child(even) {
                background: #F8F8F8;
            }
        </style>
        <div id="e40b9887eb434e3b981eeb616e6e8358" class="chart-container" style="position: absolute; width: 475px; height: 877px; top: 37px; left: 111px;">
            <p class="title" style="font-size: 18px; font-weight:bold;" > 福建GDP数据</p>
            <p class="subtitle" style="font-size: 12px;" > </p>
            <table class="fl-table">
    <thead>
        <tr>
            <th>地区</th>
            <th>GDP（亿元）</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>福州市</td>
            <td>11324.48</td>
        </tr>
        <tr>
            <td>厦门市</td>
            <td>7033.89</td>
        </tr>
        <tr>
            <td>三明市</td>
            <td>2702.19</td>
        </tr>
        <tr>
            <td>泉州市</td>
            <td>10376.76</td>
        </tr>
        <tr>
            <td>漳州市</td>
            <td>5025.4</td>
        </tr>
        <tr>
            <td>南平市</td>
            <td>2007.4</td>
        </tr>
        <tr>
            <td>龙岩市</td>
            <td>3081.78</td>
        </tr>
        <tr>
            <td>宁德市</td>
            <td>3151.08</td>
        </tr>
    </tbody>
</table>
        </div>

<br/>    </div>
    <script>
            $('#26119098d0fe4817b054ffff4e2317b3').css('border-style', 'dashed').css('border-width', '0px');$("#26119098d0fe4817b054ffff4e2317b3>div:nth-child(1)").width("100%").height("100%");
            new ResizeSensor(jQuery('#26119098d0fe4817b054ffff4e2317b3'), function() { chart_26119098d0fe4817b054ffff4e2317b3.resize()});
            $('#e40b9887eb434e3b981eeb616e6e8358').css('border-style', 'dashed').css('border-width', '0px');$("#e40b9887eb434e3b981eeb616e6e8358>div:nth-child(1)").width("100%").height("100%");
            var charts_id = ['26119098d0fe4817b054ffff4e2317b3','e40b9887eb434e3b981eeb616e6e8358'];
function downloadCfg () {
    const fileName = 'chart_config.json'
    let downLink = document.createElement('a')
    downLink.download = fileName

    let result = []
    for(let i=0; i<charts_id.length; i++) {
        chart = $('#'+charts_id[i])
        result.push({
            cid: charts_id[i],
            width: chart.css("width"),
            height: chart.css("height"),
            top: chart.offset().top + "px",
            left: chart.offset().left + "px"
        })
    }

    let blob = new Blob([JSON.stringify(result)])
    downLink.href = URL.createObjectURL(blob)
    document.body.appendChild(downLink)
    downLink.click()
    document.body.removeChild(downLink)
}
    </script>
</body>
</html>
 """,
                        height=800,
                        width=1500
                        )
    elif table == '漳州空气质量指数':
        components.html("""
        <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>基于Pyecharts的可视化大屏</title>
            <script type="text/javascript" src="https://assets.pyecharts.org/assets/echarts.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/maps/fu2_jian4_zhang1_zhou1.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://assets.pyecharts.org/assets/ResizeSensor.js"></script>

            <link rel="stylesheet"  href="https://assets.pyecharts.org/assets/jquery-ui.css">

</head>
<body>
    <style>.box {  }; </style>
        
    <div class="box">
                        <style>
            .fl-table {
                margin: 20px;
                border-radius: 5px;
                font-size: 12px;
                border: none;
                border-collapse: collapse;
                max-width: 100%;
                white-space: nowrap;
                word-break: keep-all;
            }

            .fl-table th {
                text-align: left;
                font-size: 20px;
            }

            .fl-table tr {
                display: table-row;
                vertical-align: inherit;
                border-color: inherit;
            }

            .fl-table tr:hover td {
                background: #00d1b2;
                color: #F8F8F8;
            }

            .fl-table td, .fl-table th {
                border-style: none;
                border-top: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-bottom: 3px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                padding: .5em .55em;
                font-size: 15px;
            }

            .fl-table td {
                border-style: none;
                font-size: 15px;
                vertical-align: center;
                border-bottom: 1px solid #dbdbdb;
                border-left: 1px solid #dbdbdb;
                border-right: 1px solid #dbdbdb;
                height: 30px;
            }

            .fl-table tr:nth-child(even) {
                background: #F8F8F8;
            }
        </style>
        <div id="1c4381efa2cb4150ae4a74e4cba7e153" class="chart-container" style="position: absolute; width: 339px; height: 857px; top: 31px; left: 8px;">
            <p class="title" style="font-size: 18px; font-weight:bold;" > 漳州空气指数数据</p>
            <p class="subtitle" style="font-size: 12px;" > </p>
            <table class="fl-table">
    <thead>
        <tr>
            <th>地区</th>
            <th>空气指数</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>芗城区</td>
            <td>2.55</td>
        </tr>
        <tr>
            <td>龙文区</td>
            <td>2.64</td>
        </tr>
        <tr>
            <td>龙海区</td>
            <td>2.88</td>
        </tr>
        <tr>
            <td>长泰区</td>
            <td>2.58</td>
        </tr>
        <tr>
            <td>漳浦县</td>
            <td>2.45</td>
        </tr>
        <tr>
            <td>云霄县</td>
            <td>2.3</td>
        </tr>
        <tr>
            <td>诏安县</td>
            <td>2.41</td>
        </tr>
        <tr>
            <td>东山县</td>
            <td>2.46</td>
        </tr>
        <tr>
            <td>平和县</td>
            <td>2.75</td>
        </tr>
        <tr>
            <td>南靖县</td>
            <td>2.35</td>
        </tr>
        <tr>
            <td>华安县</td>
            <td>2.15</td>
        </tr>
        <tr>
            <td>漳州开发区</td>
            <td>2.72</td>
        </tr>
        <tr>
            <td>常山开发区</td>
            <td>2.66</td>
        </tr>
        <tr>
            <td>古雷开发区</td>
            <td>2.86</td>
        </tr>
        <tr>
            <td>台商投资区</td>
            <td>2.54</td>
        </tr>
        <tr>
            <td>漳州高新区</td>
            <td>2.39</td>
        </tr>
    </tbody>
</table>
        </div>

<br/>                <div id="738a072bc22742e186a826096a418f06" class="chart-container" style="position: absolute; width: 1376px; height: 840px; top: 49px; left: 350px;"></div>
    <script>
        var chart_738a072bc22742e186a826096a418f06 = echarts.init(
            document.getElementById('738a072bc22742e186a826096a418f06'), 'white', {renderer: 'canvas'});
        var option_738a072bc22742e186a826096a418f06 = {
    "animation": true,
    "animationThreshold": 2000,
    "animationDuration": 1000,
    "animationEasing": "cubicOut",
    "animationDelay": 0,
    "animationDurationUpdate": 300,
    "animationEasingUpdate": "cubicOut",
    "animationDelayUpdate": 0,
    "color": [
        "#c23531",
        "#2f4554",
        "#61a0a8",
        "#d48265",
        "#749f83",
        "#ca8622",
        "#bda29a",
        "#6e7074",
        "#546570",
        "#c4ccd3",
        "#f05b72",
        "#ef5b9c",
        "#f47920",
        "#905a3d",
        "#fab27b",
        "#2a5caa",
        "#444693",
        "#726930",
        "#b2d235",
        "#6d8346",
        "#ac6767",
        "#1d953f",
        "#6950a1",
        "#918597"
    ],
    "series": [
        {
            "type": "map",
            "name": "\u6f33\u5dde\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570",
            "label": {
                "show": true,
                "position": "top",
                "color": "blue",
                "margin": 8
            },
            "mapType": "\u6f33\u5dde",
            "data": [
                {
                    "name": "\u8297\u57ce\u533a",
                    "value": 2.55
                },
                {
                    "name": "\u9f99\u6587\u533a",
                    "value": 2.64
                },
                {
                    "name": "\u9f99\u6d77\u533a",
                    "value": 2.88
                },
                {
                    "name": "\u957f\u6cf0\u533a",
                    "value": 2.58
                },
                {
                    "name": "\u6f33\u6d66\u53bf",
                    "value": 2.45
                },
                {
                    "name": "\u4e91\u9704\u53bf",
                    "value": 2.3
                },
                {
                    "name": "\u8bcf\u5b89\u53bf",
                    "value": 2.41
                },
                {
                    "name": "\u4e1c\u5c71\u53bf",
                    "value": 2.46
                },
                {
                    "name": "\u5e73\u548c\u53bf",
                    "value": 2.75
                },
                {
                    "name": "\u5357\u9756\u53bf",
                    "value": 2.35
                },
                {
                    "name": "\u534e\u5b89\u53bf",
                    "value": 2.15
                },
                {
                    "name": "\u6f33\u5dde\u5f00\u53d1\u533a",
                    "value": 2.72
                },
                {
                    "name": "\u5e38\u5c71\u5f00\u53d1\u533a",
                    "value": 2.66
                },
                {
                    "name": "\u53e4\u96f7\u5f00\u53d1\u533a",
                    "value": 2.86
                },
                {
                    "name": "\u53f0\u5546\u6295\u8d44\u533a",
                    "value": 2.54
                },
                {
                    "name": "\u6f33\u5dde\u9ad8\u65b0\u533a",
                    "value": 2.39
                }
            ],
            "roam": true,
            "aspectScale": 0.75,
            "nameProperty": "name",
            "selectedMode": false,
            "zoom": 1,
            "mapValueCalculation": "sum",
            "showLegendSymbol": true,
            "emphasis": {},
            "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
            }
        }
    ],
    "legend": [
        {
            "data": [
                "\u6f33\u5dde\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570"
            ],
            "selected": {
                "\u6f33\u5dde\u7a7a\u6c14\u8d28\u91cf\u7efc\u5408\u6307\u6570": true
            },
            "show": true,
            "padding": 5,
            "itemGap": 10,
            "itemWidth": 25,
            "itemHeight": 14
        }
    ],
    "tooltip": {
        "show": true,
        "trigger": "item",
        "triggerOn": "mousemove|click",
        "axisPointer": {
            "type": "line"
        },
        "showContent": true,
        "alwaysShowContent": false,
        "showDelay": 0,
        "hideDelay": 100,
        "textStyle": {
            "fontSize": 14
        },
        "borderWidth": 0,
        "padding": 5
    },
    "title": [
        {
            "text": "\u57ce\u5e02\u5730\u56fe",
            "padding": 5,
            "itemGap": 10
        }
    ],
    "visualMap": {
        "show": true,
        "type": "continuous",
        "min": 2.0,
        "max": 2.6,
        "inRange": {
            "color": [
                "#50a3ba",
                "#eac763",
                "#d94e5d"
            ]
        },
        "calculable": true,
        "inverse": false,
        "splitNumber": 5,
        "orient": "vertical",
        "showLabel": true,
        "itemWidth": 20,
        "itemHeight": 140,
        "borderWidth": 0
    }
};
        chart_738a072bc22742e186a826096a418f06.setOption(option_738a072bc22742e186a826096a418f06);
    </script>
<br/>    </div>
    <script>
            $('#1c4381efa2cb4150ae4a74e4cba7e153').css('border-style', 'dashed').css('border-width', '0px');$("#1c4381efa2cb4150ae4a74e4cba7e153>div:nth-child(1)").width("100%").height("100%");
            $('#738a072bc22742e186a826096a418f06').css('border-style', 'dashed').css('border-width', '0px');$("#738a072bc22742e186a826096a418f06>div:nth-child(1)").width("100%").height("100%");
            new ResizeSensor(jQuery('#738a072bc22742e186a826096a418f06'), function() { chart_738a072bc22742e186a826096a418f06.resize()});
            var charts_id = ['1c4381efa2cb4150ae4a74e4cba7e153','738a072bc22742e186a826096a418f06'];
function downloadCfg () {
    const fileName = 'chart_config.json'
    let downLink = document.createElement('a')
    downLink.download = fileName

    let result = []
    for(let i=0; i<charts_id.length; i++) {
        chart = $('#'+charts_id[i])
        result.push({
            cid: charts_id[i],
            width: chart.css("width"),
            height: chart.css("height"),
            top: chart.offset().top + "px",
            left: chart.offset().left + "px"
        })
    }

    let blob = new Blob([JSON.stringify(result)])
    downLink.href = URL.createObjectURL(blob)
    document.body.appendChild(downLink)
    downLink.click()
    document.body.removeChild(downLink)
}
    </script>
</body>
</html>
""",
                        height=900,
                        width=1400
                        )
