import streamlit as st
import time
import pandas as pd
import numpy as np
import pymysql
import random

st.set_page_config(page_title='assetmanagement', layout='wide')


def get_df_from_mysql(dn):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''select * from {0}'''.format(dn)
    c.execute(sql)  # 执行SQL语句
    datas = c.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = c.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in datas], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
    # print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


def get_by_assetid(aid):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''select * from asset where 资产id = '{0}' '''.format(aid)
    c.execute(sql)  # 执行SQL语句
    datas = c.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = c.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in datas], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
    # print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


def delete_patch(_patch_code):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''delete from patch where 补丁编号 in {0} '''.format(_patch_code)
    # print(sql)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


def add_assert(_inp_asset_id, _inp_asset_name, _inp_ip_addr, _inp_mac_addr, _inp_sys_type, _inp_safe_level,
               _inp_asset_owner):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''insert into asset (资产id, 资产名称, ip地址, mac地址, 系统类型, 安全等级, 资产所属人) 
    values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')'''.format(_inp_asset_id, _inp_asset_name, _inp_ip_addr,
                                                                _inp_mac_addr, _inp_sys_type, _inp_safe_level,
                                                                _inp_asset_owner)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


def update_asset(_asset_choice, _up_asset_id, _up_asset_name, _up_ip_addr, _up_mac_addr, _up_sys_type, _up_safe_level,
                 _up_asset_owner):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''update asset set 资产id = '{0}', 资产名称 ='{1}', ip地址 ='{2}', mac地址 ='{3}',系统类型 ='{4}',安全等级 ='{5}',
    资产所属人 ='{6}' where 资产id = '{7}' '''.format(
        _up_asset_id, _up_asset_name, _up_ip_addr, _up_mac_addr, _up_sys_type, _up_safe_level, _up_asset_owner,
        _asset_choice)
    # print('>>>>>>>>', sql)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


def delete_asset(_asset_choice):
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''delete from asset where 资产id = '{0}' '''.format(_asset_choice)
    # print(sql)
    c.execute(sql)  # 执行SQL语句
    con.commit()
    c.close()
    con.close()


asset = get_df_from_mysql('asset')
patch = get_df_from_mysql('patch')

# 前端展示部分
choice = st.sidebar.radio('', ('首页', '资产管理信息', '漏洞扫描', '漏洞修复', '补丁搜集'))
if choice == '首页':
    st.title('资产概况')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("未修复资产总量", random.randint(100000, 200000))
    col2.metric("补丁库总量", random.randint(10000, 50000))
    col3.metric("本月新增补丁", random.randint(10000, 50000))
    col4.metric("本月转正补丁", random.randint(10000, 50000))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write('漏洞资产top5')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (5, 1)), columns=["资产"])
        st.bar_chart(chart_data)
    with c2:
        st.write('漏洞资产组top5')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (5, 1)), columns=["资产组"])
        st.bar_chart(chart_data)
    with c3:
        st.write('补丁更新记录')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (15, 1)), columns=["记录"])
        st.line_chart(chart_data)
    c4, c5, c6 = st.columns(3)
    with c4:
        st.write('资产风险分析')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (10, 5)), columns=["a", "b", "c", "d", "e"])
        st.area_chart(chart_data)
    with c5:
        st.write('未打补丁分布')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (10, 3)), columns=["a", "b", "c"])
        st.area_chart(chart_data)
    with c6:
        st.write('系统资源监控')
        chart_data = pd.DataFrame(np.random.randint(1000, 10000, (15, 3)), columns=["a", "b", "c"])
        st.line_chart(chart_data)
elif choice == '资产管理信息':
    st.title('资产管理信息')
    # tab1, tab2 = st.tabs(["资产发现", "资产信息"])
    tab = st.selectbox('', ["资产发现", "资产信息"])
    # with tab1:
    if tab == '资产发现':
        st.subheader('资产发现')
        ips = st.text_input('IP探测：', '请输入IP地址、IP段或IP掩码')
        # sct = st.text_input('扫描时间间隔：', 'S或s为秒，M或m为分钟，H或h为小时，无单位为分钟')
        scan = st.button('立即执行网段扫描')
        if scan:
            if '请输入IP地址、IP段或IP掩码' in ips or len(ips) == 0:
                st.warning('请输入有效ip')
            else:
                my_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1)
                st.success('扫描成功！')
                st.metric('主机', 'hostname' + str(random.randint(1, 10)))
                st.metric('系统类型', 'centos0' + str(random.randint(1, 9)))
    # with tab2:
    elif tab == '资产信息':
        st.subheader('资产信息查询')
        c1, c2, c3, c4 = st.columns(4)
        assetid = list(set(asset['资产id']))
        assetid.append('')
        systemtype = list(set(asset['系统类型']))
        systemtype.append('')
        ipaddress = list(set(asset['ip地址']))
        ipaddress.append('')
        safetylevel = list(set(asset['安全等级']))
        safetylevel.append('')
        with c1:
            asset_id = st.selectbox('资产id', assetid, index=len(assetid) - 1)
        with c2:
            ip_address = st.selectbox('ip地址', ipaddress, index=len(ipaddress) - 1)
        with c3:
            system_type = st.selectbox('系统类型', systemtype, index=len(systemtype) - 1)
        with c4:
            safety_level = st.selectbox('安全等级', safetylevel, index=len(safetylevel) - 1)
        query = st.button('开始查询')
        if query:
            if asset_id == '' and ip_address == '' and system_type == '' and safety_level == '':
                st.table(asset)
            else:
                asset_df = asset[(asset['资产id'] == asset_id) | (asset['ip地址'] == ip_address) |
                                 (asset['系统类型'] == system_type) | (asset['安全等级'] == safety_level)]
                st.table(asset_df)
        st.subheader("添加、修改、删除资产信息")
        user_action = st.selectbox(
            "请选择操作",
            ["添加", "修改", "删除"]
        )
        if user_action:
            # with st.form(user_action):
            if user_action == "添加":
                c1, c2 = st.columns(2)
                with c1:
                    inp_asset_id = st.text_input("资产id")
                    inp_asset_name = st.text_input("资产名称")
                    inp_ip_addr = st.text_input("ip地址")
                    inp_mac_addr = st.text_input("mac地址")
                with c2:
                    inp_sys_type = st.text_input("系统类型")
                    inp_safe_level = st.text_input("安全等级")
                    inp_asset_owner = st.text_input("资产所属人")
                # submitted = st.form_submit_button("提交")
                submitted = st.button("提交")
                if submitted:
                    # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                    add_assert(inp_asset_id, inp_asset_name, inp_ip_addr, inp_mac_addr, inp_sys_type,
                               inp_safe_level, inp_asset_owner)
                    st.success("添加成功")
            elif user_action == "修改":
                asset_choice = st.selectbox('选择要修改的资产', assetid)
                one_df = get_by_assetid(asset_choice)
                c3, c4 = st.columns(2)
                with c3:
                    up_asset_id = st.text_input("资产id", one_df['资产id'][0])
                    up_asset_name = st.text_input("资产名称", one_df['资产名称'][0])
                    up_ip_addr = st.text_input("ip地址", one_df['ip地址'][0])
                    up_mac_addr = st.text_input("mac地址", one_df['mac地址'][0])
                with c4:
                    up_sys_type = st.text_input("系统类型", one_df['系统类型'][0])
                    up_safe_level = st.text_input("安全等级", one_df['安全等级'][0])
                    up_asset_owner = st.text_input("资产所属人", one_df['资产所属人'][0])
                # submitted = st.form_submit_button("提交")
                submitted = st.button("提交")
                if submitted:
                    # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                    update_asset(str(asset_choice), str(up_asset_id), str(up_asset_name), str(up_ip_addr),
                                 str(up_mac_addr), str(up_sys_type), str(up_safe_level), str(up_asset_owner))
                    st.success("修改成功")

            else:
                asset_choice = st.selectbox('选择要删除的用户', assetid, index=len(assetid) - 1)
                # submitted = st.form_submit_button("提交")
                submitted = st.button("提交")
                if submitted:
                    # 请在这里添加真实业务逻辑，或者单独写一个业务逻辑函数
                    delete_asset(asset_choice)
                    st.success("删除成功")

elif choice == '漏洞扫描':
    st.title('漏洞扫描')
    st.header('扫描前')
    host = st.text_input('主机', '请输入主机名')
    scan = st.button('立即执行漏洞扫描')
    if scan:
        if '请输入主机名' in host or len(host) == 0:
            st.warning('请输入有效主机名')
        else:
            # 此处可以添加调用后端实际执行漏洞扫描的程序 参数为 主机 host
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            st.success('漏洞扫描成功！')
            st.header('扫描后')
            cev_df = pd.DataFrame(np.random.randint(1000, 10000, (random.randint(1, 50), 1)), columns=["cev编号"])
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("漏洞扫描结果展示")
                st.dataframe(cev_df)
            with c2:
                st.subheader('安全等级划分')
                total = len(cev_df)
                st.write('cev总数量：' + str(total))
                if total < 5:
                    st.write('安全等级为: 低')
                elif 5 <= total < 20:
                    st.write('安全等级为: 中')
                else:
                    st.write('安全等级: 高')

# elif choice == '漏洞收集':
#     st.title('漏洞收集')
#     ips = st.text_input('IP探测：', '请输入IP地址、IP段或IP掩码')
#     sct = st.text_input('收集时间间隔：', 'S或s为秒，M或m为分钟，H或h为小时，无单位为分钟')
#     collect = st.button('立即执行漏洞收集')
#     if collect:
#         my_bar = st.progress(0)
#         for percent_complete in range(100):
#             time.sleep(0.01)
#             my_bar.progress(percent_complete + 1)
#         st.success('漏洞收集成功！')
elif choice == '漏洞修复':
    st.title('漏洞修复')
    host = st.text_input('主机', '请输入主机名')
    fix = st.button('立即执行漏洞修复')
    if fix:
        if '请输入主机名' in host or len(host) == 0:
            st.warning('请输入有效主机名')
        else:
            # 此处可以添加调用后端实际执行漏洞修复的程序  参数为 host
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            st.success('漏洞修复成功！')
elif choice == '补丁搜集':
    st.title('补丁搜集')
    st.subheader('补丁更新')
    self_define = st.text_input('自定义参数', '请输入一个参数')
    update = st.button('立即执行更新')
    if update:
        if '请输入一个参数' in self_define or len(self_define) == 0:
            st.warning('请输入有效参数')
        else:
            # 此处可以添加调用后端实际执行自动更新的程序  参数为 self_define
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            # 如果自动更新程序成功 则 返回自动更新成功 否则 返回自动更新失败
            st.success('自动更新成功！')
    st.subheader('补丁查询')
    c1, c2, c3, c4 = st.columns(4)
    patchcodes = list(set(patch['补丁编号']))
    patchcodes.append('')
    dangerlevels = list(set(patch['危险等级']))
    dangerlevels.append('')
    fitsystems = list(set(patch['适应操作系统']))
    fitsystems.append('')
    publicdates = list(set(patch['发布时间']))
    publicdates.append('')
    with c1:
        patch_code = st.selectbox('补丁编号', patchcodes, index=len(patchcodes) - 1)
    with c2:
        danger_level = st.selectbox('危险等级', dangerlevels, index=len(dangerlevels) - 1)
    with c3:
        fit_system = st.selectbox('适应操作系统', fitsystems, index=len(fitsystems) - 1)
    with c4:
        public_date = st.selectbox('发布时间', publicdates, index=len(publicdates) - 1)
    query = st.button('开始查询')
    if query:
        if patch_code == '' and danger_level == '' and fit_system == '' and public_date == '':
            st.table(patch)
        else:
            patch_df = patch[(patch['补丁编号'] == patch_code) | (patch['危险等级'] == danger_level) |
                             (patch['适应操作系统'] == fit_system) | (patch['发布时间'] == public_date)]
            st.table(patch_df)

    patch_code = st.multiselect('选择要删除整条记录的补丁编号', patchcodes)
    patch_codes = str(patch_code).replace('[', '(').replace(']', ')')
    # print(patch_codes)
    delete = st.button('确认删除')
    if delete:
        delete_patch(patch_codes)
        st.success('成功删除数据！')
