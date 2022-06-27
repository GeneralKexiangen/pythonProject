import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import copy
import sys
from math import radians, cos, sin, asin, sqrt


class Ant(object):
    # 初始化
    def __init__(self, ID, distance_graph, pheromone_graph, ALPHA, BETA):
        self.city_num = len(distance_graph)
        self.distance_graph = distance_graph  # 距离矩阵
        self.pheromone_graph = pheromone_graph  # 信息素矩阵
        self.ID = ID  # ID
        (self.ALPHA, self.BETA) = (ALPHA, BETA)  # 蚂蚁在选择路径时  信息素与距离反比的比重
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.open_table_city = [True for i in range(self.city_num)]  # 探索城市的状态
        if self.city_num > 2:  # 如果商店数目大于2那么就不能走city[1]
            self.open_table_city[1] = False
        # city_index = random.randint(0, self.city_num - 1)  # 随机初始出生点
        city_index = 0  # 初始点是开始点
        self.current_city = city_index
        self.path.append(city_index)  # 这只蚂蚁经过的路径
        self.open_table_city[city_index] = False  # 城市是否无访问
        self.move_count = 1

    # 选择下一个城市
    def _choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for i in range(self.city_num)]  # 选择城市的可能性
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(self.city_num):
            if self.open_table_city[i]:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(self.pheromone_graph[self.current_city][i], self.ALPHA) * pow(
                        (1.0 / (self.distance_graph[self.current_city][i] + 0.00001)), self.BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
                                                                                                current=self.current_city,
                                                                                                target=i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.city_num):
                if self.open_table_city[i]:  # 如果城市没有被访问
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        # 未从概率产生，顺序选择一个未访问城市 如果temp_prob恰好选择了total_prob那么就在所有未去的城市中选择一个去的城市
        if next_city == -1:
            for i in range(self.city_num):
                if self.open_table_city[i]:
                    next_city = i
                    break

        # 返回下一个城市序号
        return next_city

    # 移动操作
    def _move(self, next_city):
        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.current_city = next_city
        self.move_count += 1

    # 翻转操作
    def _reverse(self, start, end):  # 表示是protect函数
        # self.path[start:end+1]=self.path[end:start-1:-1]   #从bc  变成cb
        tmpPath = self.path.copy()
        tmpPath[start:end + 1] = tmpPath[end:start - 1:-1]
        return tmpPath

    def _cal_lenth(self, path):
        temp_distance = 0.0
        for i in range(1, len(path)):
            start, end = path[i], path[i - 1]
            temp_distance += self.distance_graph[start][end]
        return temp_distance

    def _need_reverse(self, start, end):
        tmpPath = self.path[start - 1:end + 2].copy()
        tmpPath[1:-1] = tmpPath[-2:0:-1]
        return self._cal_lenth(tmpPath) < self._cal_lenth(self.path[start - 1:end + 2])

    # 搜索路径
    def search_path(self):
        # 搜素路径，遍历完所有城市为止
        while self.move_count < self.city_num:
            # 移动到下一个城市
            next_city = self._choice_next_city()
            self._move(next_city)
            if self.move_count == self.city_num - 1:  # 最后一个城市选择终点城市
                self.open_table_city[1] = True

        # 计算路径总长度
        self.total_distance = self._cal_lenth(self.path)

        i = 2  # 步长
        while i < self.city_num - 1:
            j = 1  # 起始位置
            while j < self.city_num - i:
                if self._need_reverse(j, i + j - 1):
                    self.path = self._reverse(j, i + j - 1)  # 得到翻转之后的路径
                    self.total_distance = self._cal_lenth(self.path)  # 更新总长度
                    i = 2  # 重做整个结果
                    j = 1
                j += 1
            i += 1


class tsp(object):

    def __init__(self, data_set):  # data_set是所有点的经纬度坐标，label_list是这个分组的编号序列
        self.cities = data_set  # 商店的地址（经纬度信息）
        self.maxIter = 1  # 蚁群算法的最大迭代次数
        self.rootNum = data_set.shape[0]  # 本分组的商店的数目
        (self.city_num, self.ant_num) = (self.rootNum, 30)
        (self.ALPHA, self.BETA, self.RHO, self.Q) = (1.0, 9.0, 0.5, 100.0)  # 蚁群算法参数
        self.distance_graph = [[0.0 for i in range(self.city_num)] for j in range(self.city_num)]
        self.pheromone_graph = [[1.0 for i in range(self.city_num)] for j in range(self.city_num)]
        self.get_Dis_Pherom()  # 初始化距离
        self.new()

    def transf_Dist(self, lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r * 1000

    def get_Dis_Pherom(self):
        # 初始化城市距离
        for i in range(self.city_num):
            for j in range(self.city_num):
                self.distance_graph[i][j] = self.transf_Dist(self.cities[i, 0], self.cities[i, 1], self.cities[j, 0],
                                                             self.cities[j, 1])

    def new(self, evt=None):
        # 初始化信息素
        self.ants = [Ant(ID, self.distance_graph, self.pheromone_graph, self.ALPHA, self.BETA) for ID in
                     range(self.ant_num)]  # 初始蚁群
        self.best_ant = self.ants[-1]  # 初始最优解
        self.best_ant.total_distance = (1 << 31)  # 初始最大距离
        self.iter = 0  # 初始化迭代次数

    def search_path(self, evt=None):
        while self.iter < self.maxIter:
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
            # 更新信息素
            self.update_pheromone_gragh()
            # print("迭代次数：", self.iter, u"最佳路径总距离：", int(self.best_ant.total_distance))
            # self.draw()
            self.iter += 1
        # self.draw()
        return self.best_ant.path

    def update_pheromone_gragh(self):
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(self.city_num)] for raw in range(self.city_num)]
        for ant in self.ants:
            for i in range(1, self.city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += self.Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(self.city_num):
            for j in range(self.city_num):
                self.pheromone_graph[i][j] = self.pheromone_graph[i][j] * self.RHO + temp_pheromone[i][j]


def show_city(datas):
    matplotlib.rc("font", family='Heiti TC')  # 用来正常显示中文标签
    plt.scatter(datas[:, 0], datas[:, 1], alpha=0.6, c="r")  # 绘制散点图，透明度为0.6（这样颜色浅一点，比较好看）
    plt.title('小区分布图')
    plt.xlabel('经度（度）')
    plt.ylabel('维度（度）')
    plt.savefig('小区分布图.jpg')
    plt.show()


def show_best_way(cities, bestPath):
    matplotlib.rc("font", family='Heiti TC')
    city_num = cities.shape[0]
    ax = plt.subplot(111)
    ax.plot(cities[:, 0], cities[:, 1], 'x', color='blue')
    ax.plot(cities[0, 0], cities[0, 1], 'ro')
    ax.plot(cities[1, 0], cities[1, 1], 'ro')
    for i in range(city_num):
        ax.text(cities[i, 0], cities[i, 1], str(i))
    ax.plot(cities[bestPath, 0], cities[bestPath, 1], color='red')
    plt.title('最短路线图')
    plt.xlabel('经度（度）')
    plt.ylabel('维度（度）')
    plt.savefig('最短路线图.jpg')
    plt.show()


def notInList(lon, lat, pointList):
    for i in range(0, len(pointList)):
        if abs(lon - pointList[i][0]) <= 0.000001 and abs(lat - pointList[i][1]) <= 0.000001:
            return i
    return len(pointList)


def get_route(startlon, startlat, endlon, endlat, pointdarry):
    pointList = pointdarry.tolist()
    datas = pointList.copy()
    datas.append([startlon, startlat])
    datas.append([endlon, endlat])
    # 画出小区分布图
    show_city(np.array(datas))
    listLen = len(pointList)
    sameIndex = notInList(startlon, startlat, pointList)
    if sameIndex < listLen:
        pointList.pop(sameIndex)
    sameIndex = notInList(endlon, endlat, pointList)
    if sameIndex < listLen:
        pointList.pop(sameIndex)
    coordinateList = [[startlon, startlat], [endlon, endlat]]
    coordinateList += pointList
    dataSet = np.array(coordinateList)
    # 获取最佳路线
    pathList = tsp(dataSet).search_path()
    # 画出最佳路线图
    show_best_way(dataSet, pathList)
    resultList = []
    for i in range(len(pathList)):
        if i > 0:
            if coordinateList[pathList[i]][0] == coordinateList[pathList[i - 1]][0] \
                    and coordinateList[pathList[i]][1] == coordinateList[pathList[i - 1]][1]:
                continue
            else:
                resultList.append(coordinateList[pathList[i]])
        else:
            resultList.append(coordinateList[pathList[i]])
    return resultList


if __name__ == '__main__':
    # 除起点和终点外的小区位置数据
    data_set = [[117.162744, 36.657196], [117.157067, 36.655488], [117.160651, 36.650515]]
    data_set = np.array(data_set)
    # 其中第0个点是起点，第1个点是终点，获取最佳路径
    resultList = get_route(117.170703, 36.646714, 117.169554, 36.658701, data_set)
    print(resultList)
    print(len(resultList))
