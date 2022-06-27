from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import main_db
import pandas as pd

# 指标计算函数
dataset = main_db.get_df_from_mysql()
dataset.dropna(inplace=True)
dataset['tag'] = dataset['tag'].apply(
    lambda x: 0 if x == 'UD' else (1 if x == 'D' else (2 if x == 'O' else (3 if x == 'U' else 4))))
x = ['speed', 'vehicle_state',
     'charging_status', 'total_volt', 'total_current', 'mileage',
     'standard_soc', 'max_cell_volt', 'max_volt_cell_id', 'min_cell_volt',
     'min_cell_volt_id', 'max_temp', 'max_temp_probe_id', 'min_temp',
     'min_temp_probe_id', 'max_alarm_lvl', 'gen_alarm_sign',
     'bat_fault_list', 'isulate_r', 'dcdc_stat', 'sing_temp_num', 'gear']

y = ['tag']
data = dataset.copy()

import seaborn as sns


def fig_corr():
    corr = dataset.corr()
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(corr, annot=True, cbar_kws={'label': 'heatmap'}, ax=ax)
    return fig


# 划分训练测试集
xtrain, xtest, ytrain, ytest = train_test_split(data[x].values, data[y].values,
                                                random_state=42,
                                                test_size=0.2)
svc = SVC()
svc.fit(xtrain, ytrain)
pred = svc.predict(xtrain)
pred_test = svc.predict(xtest)
data['tag_svm_pred'] = svc.predict(data[x].values)
# SVM训练集
svm_train = []
svm_train.append(f'{accuracy_score(ytrain, pred)}')
svm_train.append('{}'.format(precision_score(ytrain, pred, average='micro')))
svm_train.append('{}'.format(recall_score(ytrain, pred, average='micro')))
svm_train.append('{}'.format(f1_score(ytrain, pred, average='micro')))
# SVM测试集
svm_test = []
svm_test.append(f'{accuracy_score(ytest, pred_test)}')
svm_test.append('{}'.format(precision_score(ytest, pred_test, average='micro')))
svm_test.append('{}'.format(recall_score(ytest, pred_test, average='micro')))
svm_test.append('{}'.format(f1_score(ytest, pred_test, average='micro')))

svc = XGBClassifier()
svc.fit(xtrain, ytrain)
pred = svc.predict(xtrain)
pred_test = svc.predict(xtest)
data['tag_xgb_pred'] = svc.predict(data[x].values)
# xgb训练集
xgb_train = []
xgb_train.append(f'{accuracy_score(ytrain, pred)}')
xgb_train.append('{}'.format(precision_score(ytrain, pred, average='micro')))
xgb_train.append('{}'.format(recall_score(ytrain, pred, average='micro')))
xgb_train.append('{}'.format(f1_score(ytrain, pred, average='micro')))
# xgb测试集
xgb_test = []
xgb_test.append(f'{accuracy_score(ytest, pred_test)}')
xgb_test.append('{}'.format(precision_score(ytest, pred_test, average='micro')))
xgb_test.append('{}'.format(recall_score(ytest, pred_test, average='micro')))
xgb_test.append('{}'.format(f1_score(ytest, pred_test, average='micro')))

result = pd.DataFrame({'svm_train': svm_train, 'svm_test': svm_test, 'xgb_train': xgb_train, 'xgb_test': xgb_test},
                      index=['accuracy', 'precision', 'recall', 'f1_score'])

import matplotlib.pyplot as plt
import numpy as np


def get_pred_df():
    pred_df = data[['tag_svm_pred', 'tag_xgb_pred', 'tag']]
    pred_df['tag_svm_pred']= pred_df['tag_svm_pred'].apply(
        lambda x: 'UD'if x == 0 else ('D' if x ==1 else ('O' if x ==2  else ('U' if x == 3 else 'OD'))))
    pred_df['tag_xgb_pred'] = pred_df['tag_xgb_pred'].apply(
        lambda x: 'UD'if x == 0 else ('D' if x ==1 else ('O' if x ==2  else ('U' if x == 3 else 'OD'))))
    pred_df['tag'] = pred_df['tag'].apply(
        lambda x: 'UD'if x == 0 else ('D' if x ==1 else ('O' if x ==2  else ('U' if x == 3 else 'OD'))))
    return pred_df


def fig_xgb():
    # 构造数据
    y1 = result.svm_train.values
    y2 = result.xgb_train.values
    xx = np.arange(len(y1))
    xx = xx * 2
    # 设置柱状图的宽度
    width = 0.5

    # 绘图
    fig = plt.figure(figsize=(16, 8))

    plt.bar(x=xx, height=y1.astype('float16'), width=width, label='SVM')
    plt.bar(x=xx + width, height=y2.astype('float16'), width=width, label='xgb')

    # 添加图标题和图例
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.xticks(xx + width * 0.5, ['accuracy', 'precision', 'recall', 'f1_score'])
    plt.legend(fontsize=15)
    plt.savefig('整个模型对比图.png', dpi=500)
    plt.tick_params(labelsize=15)
    # plt.show()
    return fig
