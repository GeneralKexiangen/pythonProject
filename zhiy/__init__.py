import pandas as pd

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

if __name__ == '__main__':
    create_partitions()






