import random
import math
import pandas as pd
import json
import os

class ItemBasedCF:
    def __init__(self, datafile=None):
        self.datafile = datafile
        self.readData()
        self.splitData(3, 47)

    def readData(self, datafile=None):
        """
        从数据文件里读取数据集合
        """
        self.datafile = datafile or self.datafile
        self.data = []
        df = pd.read_csv(self.datafile)
        self.userids = set()
        i = 0
        for index, row in df.iterrows():
            i += 1
            userid, itemid, record, mtime = row['userId'], row['movieId'], row['rating'], row['timestamp']
            if int(userid)>1000:
                break
            print('{0}.userId:{1}'.format(str(i), userid))
            self.data.append((userid, itemid, int(record)))
            self.userids.add(userid)

    def splitData(self, k, seed, data=None, M=8):
        """
        切分数据集
        测试数据集testdata
        训练数据集traindata
        """
        self.testdata = {}
        self.traindata = {}
        data = data or self.data
        random.seed(seed)
        for user, item, record in self.data:
            if random.randint(0, M) == k:
                self.testdata.setdefault(user, {})
                self.testdata[user][item] = record
            else:
                self.traindata.setdefault(user, {})
                self.traindata[user][item] = record

    def ItemSimilarity(self, train=None):
        """
        用户观看电影的相关性算法
        """
        train = train or self.traindata
        C = dict()
        N = dict()
        for u, items in train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                for j in items.keys():
                    if i == j:
                        continue
                    C.setdefault(i, {})
                    C[i].setdefault(j, 0)
                    C[i][j] += 1
        self.itemSimBest = dict()
        for i, related_items in C.items():
            self.itemSimBest.setdefault(i, {})
            for j, cij in related_items.items():
                self.itemSimBest[i].setdefault(j, 0)
                self.itemSimBest[i][j] = cij / math.sqrt(N[i] * N[j])

    def ItemSimilarity_IUF(self, train=None):
        """
        用户观看电影的相关性算法改进
        """
        train = train or self.traindata
        C = dict()
        N = dict()
        for u, items in train.items():
            for i in items.keys():
                N.setdefault(i, 0)
                N[i] += 1
                for j in items.keys():
                    if i == j:
                        continue
                    C.setdefault(i, {})
                    C[i].setdefault(j, 0)
                    C[i][j] += 1 / math.log(1 + len(items) * 1.0)
        self.itemSimBest = dict()
        for i, related_items in C.items():
            self.itemSimBest.setdefault(i, {})
            for j, cij in related_items.items():
                self.itemSimBest[i].setdefault(j, 0)
                self.itemSimBest[i][j] = cij / math.sqrt(N[i] * N[j])

    def recommend(self, user, train=None, k=8, nitem=10):
        '''
        :param user: 要推荐的用户id
        :param train: 训练数据集
        :param k: 设置与推荐用户相似的用户数
        :param nitem: 设置推荐电影数量
        :return: 推荐电影ID和推荐系数
        '''
        train = train or self.traindata
        rank = dict()
        ru = train.get(int(user))
        if ru is not None:
            for i, pi in ru.items():
                for j, wj in sorted(self.itemSimBest[i].items(), key=lambda x: x[1], reverse=True)[0:k]:
                    if j in ru:
                        continue
                    rank.setdefault(j, 0)
                    rank[j] += pi * wj
        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:nitem])

    def recallAndPrecision(self, train=None, test=None, k=8, nitem=10):
        """
        计算算法召回率和准确率
        """
        train = train or self.traindata
        test = test or self.testdata
        hit = 0
        recall = 0
        precision = 0
        for user in train.keys():
            tu = test.get(user, {})
            rank = self.recommend(user, train=train, k=k, nitem=nitem)
            for item, ratings in rank.items():
                if item in tu:
                    hit += 1
            recall += len(tu)
            precision += nitem
        return (hit / (recall * 1.0), hit / (precision * 1.0))

    def coverage(self, train=None, test=None, k=8, nitem=10):
        """
        计算算法覆盖率
        """
        train = train or self.traindata
        test = test or self.testdata
        recommend_items = set()
        all_items = set()
        for user in train.keys():
            for item in train[user].keys():
                all_items.add(item)
            rank = self.recommend(user, train, k=k, nitem=nitem)
            for item, ratings in rank.items():
                recommend_items.add(item)
        return len(recommend_items) / (len(all_items) * 1.0)

    def popularity(self, train=None, test=None, k=8, nitem=10):
        """
        计算算法流行度
        """
        train = train or self.traindata
        test = test or self.testdata
        item_popularity = dict()
        for user, items in train.items():
            for item in items.keys():
                item_popularity.setdefault(item, 0)
                item_popularity[item] += 1
        ret = 0
        n = 0
        for user in train.keys():
            rank = self.recommend(user, train, k=k, nitem=nitem)
            for item, ratings in rank.items():
                ret += math.log(1 + item_popularity[item])
                n += 1
        return ret / (n * 1.0)

def testRecommend(flag,user):
    '''
    :param flag: 选择相似度算法
    :param user: 用户id
    :return: 推荐电影列表
    '''
    ibcf =  ItemBasedCF(
        '/Users/zhiyue/Downloads/archive/ratings.csv')
    # ibcf.readData()
    # ibcf.splitData(4,100)
    if flag == 1:
        ibcf.ItemSimilarity()
    elif flag == 2:
        ibcf.ItemSimilarity_IUF()

    userids= ibcf.userids
    print('total userids: {0}'.format(len(userids)))
    recommend_list = {}
    for userid in userids:
        print('recommend for userId:{0}'.format(userid))
        recommend_list[int(userid)] = ibcf.recommend(userid, k = 3)
    print('total recommend list:', len(recommend_list))
    jsons = json.dumps(recommend_list)
    if os.path.exists('../moviesRecommend20220405/recommend_list.json'):
        os.remove('../moviesRecommend20220405/recommend_list.json')
    fp = open('../moviesRecommend20220405/recommend_list.json', 'w+', encoding='utf-8');
    fp.write(jsons)
    fp.close()

def testItemBasedCF():
    '''
    根据不同K值推荐算法评估比较
    :return:不同K值对应的召回率，准确率，覆盖率，流行度
    '''
    cf = ItemBasedCF(
        '/Users/zhiyue/Downloads/archive/ratings.csv')
    # cf.ItemSimilarity()
    cf.ItemSimilarity_IUF()
    print("%.13s%3s%20s%20s%20s%20s" % ("             ", 'K', "recall", 'precision', 'coverage', 'popularity'))
    for k in [5, 10, 20, 40, 80, 160]:
        recall, precision = cf.recallAndPrecision(k=k)
        coverage = cf.coverage(k=k)
        popularity = cf.popularity(k=k)
        print("%.13s%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (
        "ItemCF       ", k, recall * 100, precision * 100, coverage * 100, popularity))


def testUserBasedCF_IUF():
    '''
    改进推荐算法评估比较
    :return:对应的召回率，准确率，覆盖率，流行度
    '''
    cf = ItemBasedCF(
        '/Users/zhiyue/Downloads/archive/ratings.csv')
    cf.ItemSimilarity()
    print("%.13s%3s%20s%20s%20s%20s" % ("             ", 'K', "recall", 'precision', 'coverage', 'popularity'))
    for k in [10]:
        recall, precision = cf.recallAndPrecision(k=k)
        coverage = cf.coverage(k=k)
        popularity = cf.popularity(k=k)
        print("%.13s%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (
        "ItemCF       ", k, recall * 100, precision * 100, coverage * 100, popularity))
    cf.ItemSimilarity_IUF()
    for k in [10]:
        recall, precision = cf.recallAndPrecision(k=k)
        coverage = cf.coverage(k=k)
        popularity = cf.popularity(k=k)
        print("%.13s%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (
        "ItemCF_IUF   ", k, recall * 100, precision * 100, coverage * 100, popularity))


if __name__ == "__main__":
    x = int(input("请出入数字(1,代表基于商品推荐算法评估比较;2,代表基于商品改进推荐算法评估比较;3,代表基于商品为某用户推荐电影):"))
    if x == 1:
        testItemBasedCF()
    elif x == 2:
        testUserBasedCF_IUF()
    elif x == 3:
        y = int(input("请输入数字(1,代表为用户采用基于商品相似度算法推荐电影;2,代表为用户采用基于商品改进相似度算法推荐电影):"))
        # userid = str(input("请输入要推荐用户的id:"))
        testRecommend(y, None)

