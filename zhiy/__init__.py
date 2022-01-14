import pandas as pd
import cx_Oracle
import datetime

def shop_info():
    with open('shops.txt', 'r') as f:
        lines = f.readlines()
        list_flat = []
        values = []
        for line in lines:
            # print(line)
            if 'shop_id' not in line:
                fields = line.split('\t')
                flat = fields[2].replace('\n', '')
                if flat not in list_flat:
                    list_flat.append(flat)
                values.append([fields[0], fields[1], flat])
        print(list_flat)
        print("INSERT INTO TABLE dim_shop  VALUES ")
        for value in values:
            # print(value)
            print("({0},'{1}','{2}',{3}),"
                  .format(value[0], value[1], value[2], list_flat.index(value[2])+1))


def create_partitions():
    import datetime
    print(datetime.date.today())
    day_start = '2021-09-01'
    day_time_start = datetime.datetime.strptime(day_start, '%Y-%m-%d')
    while (day_time_start < datetime.datetime.strptime('2022-01-01', '%Y-%m-%d')):
        partition_name = str(day_time_start).replace('-', '')[0:8]
        day_time_start = day_time_start + datetime.timedelta(days=1)
        partition_value = str(day_time_start).replace('-', '')[0:8]
        # print(day_time_start)
        print('PARTITION p{0} VALUES LESS THAN ({1}) ENGINE = InnoDB,'.format(partition_name, partition_value))

def create_conn_table():
      # 引用模块cx_Oracle
    conn = cx_Oracle.connect('MRBI/Mr147258@10.10.199.32:1521/NCC1909')  # 连接数据库
    c = conn.cursor()  # 获取cursor
    x = c.execute('select sysdate from dual')  # 使用cursor进行各种操作
    x.fetchone()
    c.close()  # 关闭cursor
    conn.close()
    print('OK')

def create_data():
    with open('data.txt','r') as f:
        lines = f.readlines()
        for line in lines:
            # print(line.strip())
            line = line.strip()
            fields = line.split('\t')
            #转口
            if 'EP' == line[0:2]:
                print(
                    '''update ent_detail_b set vbdef10={0}, vbdef13={1}, vbdef11={2}, vbdef12={3} where  pk_detail_b ='{4}';'''.format(
                        fields[1], fields[2], fields[3], fields[4], fields[7]
                    )
                )
                if len(fields[5])>0:
                    dt5 =datetime.datetime.strptime(fields[5], '%Y/%m/%d').strftime('%Y-%m-%d')
                    print(
                        '''update ent_invoice set recedate= '{0}' where vbillcode ='{1}';'''.format(dt5, fields[0])
                    )
                if len(fields[6])>0:
                    dt6 = datetime.datetime.strptime(fields[6], '%Y/%m/%d').strftime('%Y-%m-%d')
                    print(
                        '''update ent_detail set vdef26= '{0}' where pk_detail ='{1}';'''.format(dt6, fields[8])
                    )
            #出口
            elif 'ES' == line[0:2]:
                print(
                    '''update et_detail_b set vbdef10={0}, vbdef14={1}, vbdef11={2}, vbdef12={3} where  pk_detail_b ='{4}';'''.format(
                        fields[1], fields[2], fields[3], fields[4], fields[7]
                    )
                )
                if len(fields[5])>0:
                    dt5 = datetime.datetime.strptime(fields[5], '%Y/%m/%d').strftime('%Y-%m-%d')
                    print(
                        '''update et_invoice set receiptdate= '{0}' where vbillcode ='{1}';'''.format(dt5, fields[0])
                    )
                if len(fields[6])>0:
                    dt6 = datetime.datetime.strptime(fields[6], '%Y/%m/%d').strftime('%Y-%m-%d')
                    print(
                        '''update et_detail set vdef24= '{0}' where pk_detail ='{1}';'''.format(dt6, fields[8])
                    )
            else:
                print(
                    '''update it_detail_b set vbdef6={0}, vbdef8={1}, vbdef9={2}, vbdef7={3} where  pk_detail_b ='{4}';'''.format(
                        fields[1], fields[2], fields[3], fields[4], fields[5]
                    )
                )





if __name__ == '__main__':
    #create_data()
    create_conn_table()






