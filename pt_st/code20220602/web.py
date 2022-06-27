import streamlit as st
import pandas as pd

st.set_page_config('网络应用系统部署方案')
st.title('多指标网络应用系统部署方案')


@st.cache
def get_df1():
    df = pd.read_excel('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/code20220602/网络各节点检索结果.xlsx')
    return df


@st.cache
def get_df2():
    df = pd.read_excel('/Users/zhiyue/PycharmProjects/pythonProject/pt_st/code20220602/网络应用系统的部署方案及方案总分.xlsx')
    return df


df1 = get_df1()
df2 = get_df2()

st.balloons()
st.subheader('网络各节点检索结果')
st.dataframe(df1)
st.subheader('网络应用系统的部署方案及方案总分')
st.dataframe(df2)
