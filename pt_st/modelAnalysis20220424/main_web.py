import streamlit as st
import main_model
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config('模型分析')


@st.cache
def get_iris_model_df():
    iris = main_model.test_iris()
    return iris


@st.cache
def get_iris_df():
    X_data, y_data = main_model.df_iris()
    df_x = pd.DataFrame(X_data, columns=['sepal length', 'sepal width', 'petal length', 'petal width'])
    df_y = pd.DataFrame(y_data, columns=['label'])
    iris_df_ = pd.concat([df_x, df_y], axis=1)
    return iris_df_


@st.cache
def get_polish_model_df():
    polish = main_model.test_polish()
    return polish


@st.cache
def get_polish_df():
    X_data, y_data = main_model.df_polish()
    polish_df_ = pd.concat([pd.DataFrame(X_data), pd.DataFrame(y_data)], axis=1)
    return polish_df_


@st.cache
def get_aba_model_df():
    aba = main_model.test_aba()
    return aba


@st.cache
def get_aba_df():
    X_data, y_data = main_model.df_aba()
    aba_df_ = pd.concat([pd.DataFrame(X_data), pd.DataFrame(y_data)], axis=1)
    return aba_df_


iris_model_df = get_iris_model_df()
iris_df = get_iris_df()
polish_model_df = get_polish_model_df()
polish_df = get_polish_df()
aba_model_df = get_aba_model_df()
aba_df = get_aba_df()


def login_user(uid, psd):
    if os.path.exists('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy'):
        # Load
        load_dict = np.load('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy',
                            allow_pickle=True).item()
        if uid not in load_dict.keys():
            st.warning('该账号未注册，请先注册后登录！')
        elif psd == load_dict[uid]:
            return True
        else:
            st.warning('输入的密码账号错误，请核查后再登录！')
    else:
        st.warning('请先注册后再登录！')


def register(uid, psd):
    if os.path.exists('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy'):
        # Load
        load_dict = np.load('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy',
                            allow_pickle=True).item()
        if uid in load_dict.keys():
            st.warning('该账号已注册请直接登录！')
        else:
            load_dict[uid] = psd
            np.save('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy', load_dict)
            st.success('已注册成功！')
    else:
        # Save
        users = {uid: psd}
        np.save('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/modelAnalysis20220424/users.npy', users)  # 注意带上后缀名
        st.success('已注册成功！')


def fig_multi_bar(index):
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', 'r', 'b']
    name_list = ['knn', 'decision_tree', 'svm', 'xgboost']
    iris_list = iris_model_df[index].to_list()
    aba_list = aba_model_df[index].to_list()
    polish_list = polish_model_df[index].to_list()
    x = list(range(len(iris_list)))
    total_width, n = 0.9, 3
    width = total_width / n

    plt.bar(x, iris_list, width=width, label='iris', color='#1f77b4')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, aba_list, width=width, label='aba', tick_label=name_list, color='#ff7f0e')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, polish_list, width=width, label='polish', color='#2ca02c')

    # 展示结果
    plt.legend()
    # plt.show()
    return fig


# 页面展示部分
menu = ['登录', '数据集', '模型分析之数据集', '模型分析之评估值', '注册']
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
    userid = st.sidebar.text_input("用户ID")
    password = st.sidebar.text_input("密码", type="password")
    if st.sidebar.button("开始登录"):
        logged_user = login_user(userid, password)
        if logged_user:
            st.session_state.count += 1
            if st.session_state.count >= 1:
                st.sidebar.success("您已成功登录！")
                st.balloons()
                st.title("数据与模型分析 ☕ ")
        else:
            st.session_state.count = 0
elif choice == '数据集':
    if st.session_state.count >= 1:
        datasets = ['鸢尾植物', '鲍鱼', '波兰公司破产']
        dataset = st.sidebar.selectbox('选择一个数据集', datasets)
        if dataset == '鸢尾植物':
            st.subheader('鸢尾植物数据集')
            st.dataframe(iris_df)
        elif dataset == '鲍鱼':
            st.subheader('鲍鱼数据集')
            st.dataframe(aba_df)
        elif dataset == '波兰公司破产':
            st.subheader('波兰公司破产数据集')
            st.dataframe(polish_df)
elif choice == '模型分析之数据集':
    if st.session_state.count >= 1:
        models = ['鸢尾植物数据集', '鲍鱼数据集', '波兰公司破产数据集']
        model = st.sidebar.selectbox('选择一个数据集', models)
        if model == '鸢尾植物数据集':
            st.subheader('各分类模型在鸢尾植物数据集的性能表现')
            st.dataframe(iris_model_df)
        elif model == '鲍鱼数据集':
            st.subheader('各分类模型在鲍鱼数据集的性能表现')
            st.dataframe(aba_model_df)
        elif model == '波兰公司破产数据集':
            st.subheader('各分类模型在波兰公司破产数据集的性能表现')
            st.dataframe(polish_model_df)
elif choice == '模型分析之评估值':
    if st.session_state.count >= 1:
        powers = ['F1值', '精确率', '准确率', '召回率', '用时']
        power = st.sidebar.selectbox('选择一个评估值', powers)
        if power == 'F1值':
            st.subheader('不同算法在不同数据集下的F1值对比')
            st.pyplot(fig_multi_bar('F1值'))
        elif power == '精确率':
            st.subheader('不同算法在不同数据集下的精确率对比')
            st.pyplot(fig_multi_bar('精确率'))
        elif power == '准确率':
            st.subheader('不同算法在不同数据集下的准确率对比')
            st.pyplot(fig_multi_bar('准确率'))
        elif power == '召回率':
            st.subheader('不同算法在不同数据集下的召回率对比')
            st.pyplot(fig_multi_bar('召回率'))
        elif power == '用时':
            st.subheader('不同算法在不同数据集下的用时对比')
            st.pyplot(fig_multi_bar('用时'))

elif choice == '注册':
    st.sidebar.subheader("注册区域")
    new_user = st.sidebar.text_input("用户ID")
    new_password = st.sidebar.text_input("密码", type="password")
    if st.sidebar.button("注册"):
        register(new_user, new_password)
