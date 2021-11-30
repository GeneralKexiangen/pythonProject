import time
import pymysql

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


if __name__ == '__main__':
    create_test_table("students")
    add_test_users(10)