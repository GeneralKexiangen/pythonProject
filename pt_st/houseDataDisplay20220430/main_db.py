import pymysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def dt_mysql(df, tn):
    # create_engine('mysql+pymysql://用户名:密码@主机/库名?charset=utf8')
    engine = create_engine('mysql+pymysql://root:root1234@localhost/test?charset=utf8')
    # table_commom=pd.read_excel(r'C:\Users\wuxian\Desktop\test.xlsx')
    # 将数据写入sql
    pd.io.sql.to_sql(df, tn, con=engine, if_exists='replace', index="False")


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
    print(df.dtypes)
    con.commit()
    c.close()
    con.close()
    # print("c.description中的内容：", columnDes)
    return df


data_sj = get_df_from_mysql('shuju')


def get_house_df():
    def f1(s):
        if len(s.split('|')) > 1:
            area = s.split('|')[1].strip()[:-1]
            try:
                area = float(area)
            except ValueError:
                area = 100
        else:
            area = 100
        return area

    def f2(s):
        attr = s.strip()
        if '满二' in attr:
            return int(0)
        elif '满五' in attr:
            return int(1)
        else:
            return np.nan

    def f3(s):
        attr = s.strip()
        if '教育' in attr:
            return int(1)
        else:
            return int(0)

    def f4(s):
        attr = s.strip()
        if '号线' in attr:
            return int(1)
        else:
            return int(0)

    def f5(s):
        if '元/㎡' not in s:
            return 0
        else:
            return int(s[:-3]) / 1000

    def f6(s):
        if '万' not in s:
            return 0
        else:
            return float(s[:-1])

    def f7(s):
        if '元/平米' not in s:
            return 0
        else:
            return int(s.replace('元/平米', '')) / 1000

    house_data = data_sj.copy()
    house_data = house_data.dropna()
    ds = data_sj.copy()
    ds = ds.rename(columns={'False': 'id'})
    dt_mysql(ds, '数据')
    house_data['面积'] = house_data['area and height'].apply(f1)
    house_data['满五/满二'] = house_data['attribute'].apply(f2)
    house_data['优质教育'] = house_data['attribute'].apply(f3)
    house_data['地铁'] = house_data['attribute'].apply(f4)

    house_data['区域均价(k/m2)'] = house_data['price_per_m2'].apply(f5)
    house_data['总价(w)'] = house_data['price'].apply(f6)
    house_data['地区均价(k/m2)'] = house_data['region_average_price'].apply(f7)

    house_data = house_data.dropna()
    house_df_name = ['city', 'region', '面积', '满五/满二', '优质教育', '地铁', '区域均价(k/m2)',
                     '地区均价(k/m2)', '总价(w)']
    house_df = house_data[house_df_name]

    names = ['面积', '地区均价(k/m2)', '区域均价(k/m2)', '总价(w)']
    for name in names:
        percentile90 = house_df[name].quantile(0.80)
        print(name + '_percentile80: %.1f' % (percentile90))
        house_df[name] = np.where(house_df[name] > percentile90, np.nan, house_df[name])

    house_df = house_df.dropna()
    print(house_df.head())
    dt_mysql(house_df, '房屋信息')
    return house_df


def all_pred(house_df):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

    cols = ['面积', '地铁', '地区均价(k/m2)', '区域均价(k/m2)']

    feature = house_df[cols].to_numpy()
    target = house_df['总价(w)'].to_numpy()

    print('feature.shape: ', feature.shape)
    print('target.shape: ', target.shape)

    train_X, test_X, train_y, test_y = train_test_split(feature, target, test_size=0.2, random_state=3)
    print('train_X.shape: ', train_X.shape)
    print('train_y.shape: ', train_y.shape)
    print('test_X.shape: ', test_X.shape)
    print('test_y.shape: ', test_y.shape)

    LR = LinearRegression()
    LR.fit(train_X, train_y)
    pred_y = LR.predict(test_X)
    mae = mean_absolute_error(test_y, pred_y)
    r2 = LR.score(test_X, test_y)
    print('mae: %.3f' % (mae))
    print('R2: %.3f' % (r2))
    print('LR.coef_: ', LR.coef_)
    print('LR.intercept_: ', LR.intercept_)

    price_hat = LR.predict(feature)
    house_df['预测价格(w)'] = price_hat
    # house_df.to_csv('pred_house_region_all.csv')
    dt_mysql(house_df, '预测房屋价格')
    return house_df


def get_house_region_df():
    data = pd.read_excel('pt_st/houseDataDisplay20220430/house price change.xls', header=None, skiprows=[0, 1])
    data['城市'] = np.nan
    city_list = [0, 14, 21, 32, 45, 57, 66, 74]
    # data.iloc[city_list,0]
    length = len(data)  # 82
    city_list.append(length)
    for i in range(0, len(city_list) - 1, 1):
        city_name = data.iloc[city_list[i], 0]
        data.loc[city_list[i]:city_list[i + 1], '城市'] = city_name

    # data = data.dropna()
    data.reset_index(drop=True, inplace=True)

    column_dict = {i: (37 - i) for i in range(1, 37, 1)}
    column_dict[0] = '行政区'
    column_dict['城市'] = '城市'

    data.rename(columns=column_dict, inplace=True)

    df_name = ['城市', '行政区'] + [i for i in range(1, 37, 1)]
    df = data[df_name]
    df = df.dropna()

    def f1(s):
        idx = s.index('元')
        price = int(s[:idx])
        return price

    # 行政区每月均价
    for i in range(1, 37, 1):
        df[i] = df[i].apply(f1)
    # 所属城市的级别

    df['城市级别'] = np.nan
    df.loc[((df['城市'] == '福州市') | (df['城市'] == '厦门市')), '城市级别'] = 1
    df.loc[((df['城市'] != '福州市') & (df['城市'] != '厦门市')), '城市级别'] = 0

    # 消费水平数据

    GDP_df = pd.read_excel('pt_st/houseDataDisplay20220430/GDP.xls')
    GDP_column = {'地区': '行政区', 'GDP（亿元）': 'GDP'}
    GDP_df.rename(columns=GDP_column, inplace=True)

    df = pd.merge(df, GDP_df, how='inner', on='行政区')
    # 空气质量

    air_df = pd.read_excel('pt_st/houseDataDisplay20220430/air_quality.xls')
    air_column = {'地区': '行政区', '空气质量综合指数': '空气质量综合指数'}
    air_df.rename(columns=air_column, inplace=True)
    air_df = air_df.dropna()
    df = pd.merge(df, air_df, how='inner', on='行政区')

    new_df_name = ['城市', '行政区', '城市级别', 'GDP', '空气质量综合指数'] + [i for i in range(1, 37, 1)]
    df = df[new_df_name]

    # df.to_csv("房屋价格变化趋势.csv")
    dt_mysql(df, '房屋价格变化趋势')
    new_df = pd.DataFrame([], columns=['城市', '行政区', '城市级别', 'GDP', '空气质量综合指数', '1', '2', '3', '4'])

    for begin_idx in range(1, 34, 1):
        index_list = ['城市', '行政区', '城市级别', 'GDP', '空气质量综合指数', begin_idx, begin_idx + 1, begin_idx + 2, begin_idx + 3]
        tmp_df = df.loc[:, index_list]
        # if begin_idx==1: print(tmp_df)
        new_index_list = ['城市', '行政区', '城市级别', 'GDP', '空气质量综合指数', '1', '2', '3', '4']
        tmp_column = {k: v for k, v in zip(index_list, new_index_list)}
        # print(tmp_column)
        tmp_df.rename(columns=tmp_column, inplace=True)
        new_df = new_df.append(tmp_df, ignore_index=True)

    print(new_df.shape)
    new_df[['城市级别', 'GDP', '空气质量综合指数', '1', '2', '3', '4']] = new_df[
        ['城市级别', 'GDP', '空气质量综合指数', '1', '2', '3', '4']].astype('float')
    # new_df = new_df.infer_objects()
    names = ['GDP', '1', '2', '3', '4']
    for name in names:
        percentile90 = new_df[name].quantile(0.80)
        print(str(name) + '_percentile80: %.1f' % (percentile90))
        new_df[name] = np.where(new_df[name] > percentile90, np.nan, new_df[name])

    return new_df


def region_pred(new_df):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
    df = get_df_from_mysql('房屋价格变化趋势')
    # names = ['GDP', '3']
    names = ['城市级别', 'GDP', '空气质量综合指数', '1', '2', '3']
    new_df = new_df.dropna()
    feature = new_df[names].to_numpy()
    target = new_df['4'].to_numpy()

    print('feature.shape: ', feature.shape)
    print('target.shape: ', target.shape)

    train_X, test_X, train_y, test_y = train_test_split(feature, target, test_size=0.2, random_state=3)
    print('train_X.shape: ', train_X.shape)
    print('train_y.shape: ', train_y.shape)
    print('test_X.shape: ', test_X.shape)
    print('test_y.shape: ', test_y.shape)

    LR = LinearRegression()
    LR.fit(train_X, train_y)
    pred_y = LR.predict(test_X)
    mae = mean_absolute_error(test_y, pred_y)
    r2 = LR.score(test_X, test_y)
    print('mae: %.3f' % (mae))
    print('R2: %.3f' % (r2))
    print('LR.coef_: ', LR.coef_)
    print('LR.intercept_: ', LR.intercept_)

    pred_df = df.copy()
    pred_df[1], pred_df[2], pred_df[3] = np.nan, np.nan, np.nan

    for begin_idx in range(1, 34, 1):
        index_list = ['城市级别', 'GDP', '空气质量综合指数', str(begin_idx), str(begin_idx + 1), str(begin_idx + 2)]
        tmp_df = df.loc[:, index_list]

        tmp_np = tmp_df.to_numpy()
        tmp_hat = LR.predict(tmp_np)
        pred_df[begin_idx + 3] = tmp_hat

    best_month = []
    for i in range(71):
        tmp = pred_df.copy().iloc[i, 8:].sort_values(ascending=True).iloc[:1].index.tolist()
        best_month.append(tmp)
    pred_df['预测最优买房月份'] = np.array(best_month)
    # pred_df.to_csv("预测房屋价格变化趋势.csv")
    pred_df = pred_df.rename(columns={'False': 'id'})
    dt_mysql(pred_df, '预测房屋价格变化趋势')
    return pred_df


if __name__ == '__main__':
    new_df = get_house_region_df()
    pred_df = region_pred(new_df)
    # df = get_df_from_mysql('预测房屋价格变化趋势')
    # print(df[df['行政区'] == '鼓楼区'].values)
    # ct =['仓山区']
    # show_data(ct)
