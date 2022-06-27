import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from scipy.io import arff
import numpy as np
# 朴素贝叶斯，KNN，决策树，向量机，逻辑回归，随机森林，GDBT，Xgboost
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from sklearn.preprocessing import MinMaxScaler
import time


# 波兰公司破产数据集
def df_polish():
    filepath = '/Users/zhiyue/Downloads/datasets/3year.arff'
    data = arff.loadarff(filepath)
    df = pd.DataFrame(data[0])
    df_polish = df.fillna(0)
    df_polish[["class"]] = df_polish[["class"]].astype(int)
    X_data, y_data = df_polish[df_polish.columns[0:-1]], df_polish['class']
    return X_data, y_data


# 鸢尾植物数据集
def df_iris():
    iris = datasets.load_iris()
    X_data = iris.data  # 特征
    y_data = iris.target  # 类别
    return X_data, y_data


# 鲍鱼数据集
def df_aba():
    names = ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight',
             'Shell weight',
             'Rings']
    df_aba = pd.read_csv('/Users/zhiyue/Downloads/datasets/abalone.data', names=names)
    df_aba['Sex'] = df_aba['Sex'].apply(lambda x: 1 if x == 'M' else (2 if x == 'F' else 3))
    df_aba['Rings'] = df_aba['Rings'].apply(lambda x: 0 if 0 <= x <= 9 else (1 if 10 <= x <= 19 else 2))
    X_data, y_data = df_aba[df_aba.columns[0:-1]], df_aba['Rings']
    return X_data, y_data


def model_after(modeln, model, test_x, test_y):
    if modeln == 'knn_self':
        pred_y = []
        for x in test_x:
            _, pred_ = model.predict(x)
            pred_y.append(pred_)
    elif modeln == 'tree_self':
        pred_y = []
        for x in test_x:
            pred_ = model.predict(x)
            if pred_ is None:
                pred_ = 0
            pred_y.append(pred_)
    elif modeln == 'svm_self':
        pred_y = []
        for x in test_x:
            pred_ = model.predict(x)
            pred_y.append(pred_)
    else:
        pred_y = model.predict(test_x)
    f1 = f1_score(test_y, pred_y, average='macro')
    p = precision_score(test_y, pred_y, average='macro')
    a = accuracy_score(test_y, pred_y)
    r = recall_score(test_y, pred_y, average='macro')
    return f1, p, a, r


class ModelRun:
    def __init__(self, model_names=None, data_name=None):
        self.model_names = model_names
        self.data_name = data_name
        self.df_aba = df_aba()
        self.df_iris = df_iris()
        self.df_polish = df_polish()
        self.train_x, self.train_y, self.test_x, self.test_y = self.generate_classification_train_data()
        # 朴素贝叶斯，KNN，决策树，向量机，逻辑回归，随机森林，GDBT，Xgboost
        # self.knn_classifier = self.knn_classifier()
        # self.knn_classifier_self = self.knn_classifier_self()
        # self.naive_bayes_classifier = self.naive_bayes_classifier()
        # self.decision_tree_classifier = self.decision_tree_classifier()
        # self.decision_tree_classifier_self = self.decision_tree_classifier_self()
        # self.svm_classifier = self.svm_classifier()
        # self.svm_classifier_self = self.svm_classifier_self()
        # self.logistic_regression_classifier = self.logistic_regression_classifier()
        # self.random_forest_classifier = self.random_forest_classifier()
        # self.gradient_boosting_classifier = self.gradient_boosting_classifier()
        # self.xgboost_classifier = self.xgboost_classifier()

    # 数据划分训练集和测试集
    def generate_classification_train_data(self):
        X_data, y_data = None, None
        if self.data_name == 'iris':
            X_data, y_data = self.df_iris
        elif self.data_name == 'polish':
            X_data, y_data = self.df_polish
        elif self.data_name == 'aba':
            X_data, y_data = self.df_aba
        # 数据预处理
        scaler = MinMaxScaler()
        X_data = scaler.fit_transform(X_data)
        train_X, test_X, train_y, test_y = train_test_split(X_data, y_data, test_size=0.2)
        train_x = np.array(train_X)
        test_x = np.array(test_X)
        train_y = np.array(train_y)
        test_y = np.array(test_y)
        return train_x, train_y, test_x, test_y

    # 各个分类模型对数据进行训练及预测
    # 朴素贝叶斯
    def naive_bayes_classifier(self):
        start_time = time.time()
        model = MultinomialNB()
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('naive', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # KNN_self
    def knn_classifier_self(self):
        start_time = time.time()
        # model = KNeighborsClassifier(n_neighbors=10)
        from knn import knn_kdtree
        model = knn_kdtree.KNNKdTree()
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('knn_self', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # KNN_sklearn
    def knn_classifier(self):
        start_time = time.time()
        model = KNeighborsClassifier(n_neighbors=10)
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('knn', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 决策树_self
    def decision_tree_classifier_self(self):
        start_time = time.time()
        # model = tree.DecisionTreeClassifier()
        from tree import trees
        dataset = pd.concat([pd.DataFrame(self.train_x), pd.DataFrame(self.train_y)], axis=1)
        cols = []
        if self.data_name == 'iris':
            cols = ['1', '2', '3', '4', '类别']
        elif self.data_name == 'aba':
            cols = ['1', '2', '3', '4', '5', '6', '7', '8', '类别']
        dataset.columns = cols
        model = trees.DTreeID3(epsilon=0)
        model.fit(dataset)
        f1, p, a, r = model_after('tree_self', model.tree, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 决策树
    def decision_tree_classifier(self):
        start_time = time.time()
        model = tree.DecisionTreeClassifier()
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('tree', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 向量机_self
    def svm_classifier_self(self):
        start_time = time.time()
        # model = SVC(kernel='rbf', probability=True)
        from svm import svms
        model = svms.SVM(max_iter=200)
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('svm_self', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 向量机
    def svm_classifier(self):
        start_time = time.time()
        model = SVC(kernel='rbf', probability=True)
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('svm', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 逻辑回归
    def logistic_regression_classifier(self):
        start_time = time.time()
        model = LogisticRegression(penalty='l2')
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('logistic', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # 随机森林
    def random_forest_classifier(self):
        start_time = time.time()
        model = RandomForestClassifier(n_estimators=8)
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('random', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # GDBT
    def gradient_boosting_classifier(self):
        start_time = time.time()
        model = GradientBoostingClassifier(n_estimators=200)
        model.fit(self.train_x, self.train_y)
        f1, p, a, r = model_after('GDBt', model, self.test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return model, f1, p, a, r, d_time

    # Xgboost
    def xgboost_classifier(self):
        start_time = time.time()
        dtrain = xgb.DMatrix(self.train_x, label=self.train_y)
        num_class = len(set(self.train_y))
        params = {'learning_rate': 0.1,
                  'max_depth': 5,
                  'objective': 'multi:softmax',
                  'random_state': 27,
                  'num_class': num_class
                  }
        num_round = 20
        bst = xgb.train(params, dtrain, num_round)
        test_x = xgb.DMatrix(self.test_x)
        f1, p, a, r = model_after('xgb', bst, test_x, self.test_y)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
        return bst, f1, p, a, r, d_time

    def model_df(self, model_names=None):
        model_result = {}
        if self.model_names is None:
            model_names = ['knn', 'decision_tree', 'svm', 'xgboost']
        for model_name in model_names:
            result = {}
            f1_ = 0
            p_ = 0
            a_ = 0
            r_ = 0
            d_time_ = 0
            for i in range(0, 2):
                if model_name == 'knn':
                    if self.data_name != 'polish':
                        f1, p, a, r, d_time = self.knn_classifier()[1:6]
                    else:
                        f1, p, a, r, d_time = self.knn_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'naive_bayes':
                    f1, p, a, r, d_time = self.naive_bayes_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'decision_tree':
                    if self.data_name != 'polish':
                        f1, p, a, r, d_time = self.decision_tree_classifier_self()[1:6]
                    else:
                        f1, p, a, r, d_time = self.decision_tree_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'svm':
                    if self.data_name != 'polish':
                        f1, p, a, r, d_time = self.svm_classifier_self()[1:6]
                    else:
                        f1, p, a, r, d_time = self.svm_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'logistic_regression':
                    f1, p, a, r, d_time = self.logistic_regression_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'random_forest':
                    f1, p, a, r, d_time = self.random_forest_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'gradient_boosting':
                    f1, p, a, r, d_time = self.gradient_boosting_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                elif model_name == 'xgboost':
                    f1, p, a, r, d_time = self.xgboost_classifier()[1:6]
                    f1_ += f1
                    p_ += p
                    a_ += a
                    r_ += r
                    d_time_ += d_time
                    # result['f1'] = f1
                    # result['p'] = p
                    # result['a'] = a
                    # result['r'] = r
                    # result['d_time'] = d_time
                else:
                    continue
            result['f1'] = f1_/2
            result['p'] = p_/2
            result['a'] = a_/2
            result['r'] = r_/2
            result['d_time'] = d_time_/2
            model_result[model_name] = result
        print(model_result)
        df_model = pd.DataFrame(model_result).T
        df_model.columns = ['F1值', '精确率', '准确率', '召回率', '用时']
        print(df_model)
        return df_model


def test_iris():
    mr = ModelRun(data_name='iris')
    iris_model_df = mr.model_df()
    return iris_model_df


def test_polish():
    mr = ModelRun(data_name='polish')
    polish_model_df = mr.model_df()
    return polish_model_df


def test_aba():
    mr = ModelRun(data_name='aba')
    aba_model_df = mr.model_df()
    return aba_model_df


if __name__ == '__main__':
    test_iris()
