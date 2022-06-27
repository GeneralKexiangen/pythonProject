import time
import pymysql
import datetime
import random

def timer(func):
    def decor(*args):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        d_time = end_time - start_time
        print("the running time is : ", d_time)
    return decor

@timer
def create_test_table(tn):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', db='test', charset='utf8')
    cursor = conn.cursor()
    sql =" create table if not exists {0} ( name varchar(50),age varchar(50),sex varchar(50),id varchar(50),cellphone varchar(50),address varchar(50),score varchar(50) )".format(tn)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print('OK')

@timer
def add_test_users(n):
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', db='test', charset='utf8')
    cursor = conn.cursor()
    for i in range(0, n):
        try:
            sql = "insert into students(name, age, sex, id, cellphone,address,score)values(%s,%s,%s,%s,%s,%s,%s)"
            param = (('Tom' + str(i), str(i), 'boy', str(10000 + i), str(1390000000+ i), 'shanghai', str(10 + i)))
            cursor.execute(sql, param)

        except Exception as e:
            return

    conn.commit()
    cursor.close()
    conn.close()
    print('OK')


@timer
def create_poc_table(tn):
    conn = pymysql.connect(host='123.60.37.235', port=30083, user='data_hubble', password='n1iAvkSZF7dvqCtt', db='data_hubble', charset='utf8')
    cursor = conn.cursor()
    sql =" create table if not exists {0} ( id int primary key auto_increment,brand varchar(50),product varchar(50),class1 varchar(50),class2 varchar(50),district varchar(50),dt varchar(50),dept1 varchar(50),dept2 varchar(50),warehouse varchar(50) ,income varchar(50),cost varchar(50),net varchar(50) )".format(tn)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print('OK')

@timer
def add_poc_data():
    brand_list = ['纳爱斯', '100年润发', '雕牌', '超能', '健爽白', '洁宝', '李字', '西亚斯', '妙管家', '西丽', '伢牙乐']
    product_list = ['雕牌洗衣液', '健爽白', '雕牌透明皂', '雕牌洗洁精', '超能洗衣液']
    class1_list = ['A', 'B', 'C', 'D']
    class2_list = ['a', 'b', 'c', 'd']
    district_list = ['华东大区', '华北大区', '西北大区', '华中大区', '华南大区']
    dept1_list = ['人事部', '财务部', '管理部', '运营部']
    dept2_list = ['一部', '二部', '三部', '四部']
    warehouse_list = ['一仓', '二仓', '三仓', '四仓']
    conn = pymysql.connect(host='123.60.37.235', port=30083, user='data_hubble', password='n1iAvkSZF7dvqCtt', db='data_hubble', charset='utf8')
    cursor = conn.cursor()
    dt = datetime.datetime.now()
    n = 1
    while(dt.strftime('%Y-%m-%d')!= (datetime.datetime.now()+datetime.timedelta(days = -365)).strftime('%Y-%m-%d') ):
        for m in range(11):
            brand = random.choice(brand_list)
            product = random.choice(product_list)
            class1 = random.choice(class1_list)
            class2 = random.choice(class2_list)
            district = random.choice(district_list)
            dept1 = random.choice(dept1_list)
            dept2 = random.choice(dept2_list)
            warehouse = random.choice(warehouse_list)
            try:
                sql = "insert into ads_nice_finance_poc (brand, product, class1, class2, district,dt,dept1,dept2,warehouse,income,cost,net)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                income = random.randint(1000, 10000)
                cost = income*random.randint(1, 12)*0.1
                param = ((brand, product, class1, class2, district, dt.strftime('%Y-%m-%d'),dept1,dept2,warehouse,str(income),str(cost),str((income-cost)) ))
                print('插入第{0}条数据：{1}'.format(str(n), param))
                n += 1
                cursor.execute(sql, param)
            except Exception as e:
                return
        dt = dt + datetime.timedelta(days= -1)

    conn.commit()
    cursor.close()
    conn.close()
    print('OK')

if __name__ == '__main__':
    create_poc_table("ads_nice_finance_poc")
    add_poc_data()