from pyhive import hive

conn = hive.Connection(host='zhuoshini-prod-simba-03', port=10000, username='simba', database='josiny')
print('Connect Success!')

print('Start of Cleaning historical table partitions!')