
import pymysql
import pandas as pd


def get_df_from_mysql():
    con = pymysql.connect(host="localhost", user="root", password="root1234", database="test", charset="utf8")
    c = con.cursor()
    sql = '''select * from data'''
    c.execute(sql)  # 执行SQL语句
    data = c.fetchall()

    # 下面为将获取的数据转化为dataframe格式
    columnDes = c.description  # 获取连接对象的描述信息
    columnNames = [columnDes[i][0] for i in range(len(columnDes))]  # 获取列名
    df = pd.DataFrame([list(i) for i in data], columns=columnNames)  # 得到的data为二维元组，逐行取出，转化为列表，再转化为df
    df[['speed', 'vehicle_state', 'charging_status', 'total_volt', 'total_current', 'mileage', 'standard_soc', 'max_cell_volt',
        'max_volt_cell_id', 'min_cell_volt', 'min_cell_volt_id', 'max_temp', 'max_temp_probe_id',
        'min_temp', 'min_temp_probe_id', 'max_alarm_lvl', 'gen_alarm_sign', 'bat_fault_list',
        'isulate_r', 'dcdc_stat', 'sing_temp_num', 'gear']]\
        =df[['speed', 'vehicle_state', 'charging_status', 'total_volt', 'total_current', 'mileage', 'standard_soc', 'max_cell_volt',
        'max_volt_cell_id', 'min_cell_volt', 'min_cell_volt_id', 'max_temp', 'max_temp_probe_id',
        'min_temp', 'min_temp_probe_id', 'max_alarm_lvl', 'gen_alarm_sign', 'bat_fault_list',
        'isulate_r', 'dcdc_stat', 'sing_temp_num', 'gear']].apply(pd.to_numeric)
    print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


if __name__ == '__main__':
    get_df_from_mysql()
