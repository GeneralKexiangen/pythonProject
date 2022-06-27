from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import main_db


# 生成分类数据集
def generate_classification_train_data():
    # df = pd.read_csv('data.csv')
    df = main_db.get_df_from_mysql()
    df = df.fillna(0)
    df = df.drop(columns=['yr_modahrmn', 'message_type'])
    df['tag'] = df['tag'].apply(
        lambda x: 0 if x == 'UD' else (1 if x == 'D' else (2 if x == 'O' else (3 if x == 'U' else 4))))
    y_data = df['tag']
    X_data = df.drop(columns=['tag'])
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2)

    x_train = np.array(X_train)
    x_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    return x_train, y_train, x_test, y_test


# LSTM模型构建
class SequeClassifier():
    def __init__(self, units):
        self.units = units
        self.model = None

    # 构建神经网络模型：（根据各层输入输出的shape）搭建网络结构、确定损失函数、确定优化器
    def build_model(self, loss, optimizer, metrics):
        self.model = Sequential()
        self.model.add(LSTM(self.units, return_sequences=True))
        self.model.add(LSTM(self.units))
        self.model.add(Dense(5, activation='softmax'))
        # 最后一层全连接层。对于N分类问题，最后一层全连接输出个数为N个；对于回归问题，最后一层全连接层的输出为1
        # 激活函数也很重要，如果没有使用激活函数或者激活函数选择不当，很有可能产生梯度消失或梯度爆炸模型无法学习

        self.model.compile(loss=loss,
                           optimizer=optimizer,  # 优化器的选择很重要
                           metrics=metrics)


def main():
    # 1 获取训练数据集，并调整为三维输入格式
    x_train, y_train, x_test, y_test = generate_classification_train_data()
    # 二维-->三维。构建的方法：
    x_train = x_train[:, :, np.newaxis]
    x_test = x_test[:, :, np.newaxis]
    # 2 构建神经网络模型：（根据各层输入输出的shape）搭建网络结构、确定损失函数、确定优化器
    units = 128  # lstm细胞个数
    loss = "sparse_categorical_crossentropy"  # 损失函数类型
    optimizer = "adam"  # 优化器类型
    metrics = ['accuracy']  # 评估方法类型
    sclstm = SequeClassifier(units)
    sclstm.build_model(loss, optimizer, metrics)

    # 3 训练模型
    epochs = 10
    batch_size = 64
    sclstm.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    # 4 模型评估
    score = sclstm.model.evaluate(x_test, y_test, batch_size=16)
    print("model score:", score)

    # 模型应用：预测
    # proba_prediction = sclstm.model.predict(x_test)

    # 5 模型持久化，把模型保存在本地
    dirs = "model"
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    print("正在保存模型......")
    sclstm.model.save(dirs + "/classifier_model.h5")
    print("模型已保存.save path-->dirs%s" % "/classifier_model.h5")

    # 6 从指定模型保存的位置读取模型，做预测
    from tensorflow.keras.models import load_model

    read_model = load_model(dirs + "/classifier_model.h5")
    out = read_model.predict(x_test)
    print("out:%s" % out)

    # 7 保存预测与实际对照结果
    labels = ['UD', 'D', 'O', 'U', 'OD']
    pred_tag = [labels[np.argmax(re)] for re in out]
    print(pred_tag)
    pred_tag_df = pd.DataFrame(pred_tag, columns=['pred_tag'])
    print(pred_tag_df)
    y_test = ['UD' if x == 0 else ('D' if x == 1 else ('O' if x == 2 else ('U' if x == 3 else 'OD'))) for x in y_test]
    act_tag_df = pd.DataFrame(y_test, columns=['act_tag'])
    print(act_tag_df)
    df_pre_act = pd.concat([pred_tag_df, act_tag_df], axis=1)
    df_pre_act.columns = ['预测tag', '实际tag']
    df_pre_act.to_csv('pre_act_tag.csv')


if __name__ == '__main__':
    # main()
    df = pd.read_csv('pre_act_tag.csv')
    y_pred = np.array(df['预测tag'])
    y_true = np.array(df['实际tag'])
    from sklearn.metrics import f1_score, precision_score, recall_score

    f1 = f1_score(y_true, y_pred, average='macro')
    p = precision_score(y_true, y_pred, average='macro')
    r = recall_score(y_true, y_pred, average='macro')
    print('F1值：{0},准确率：{1},召回率：{2}'.format(f1, p, r))
