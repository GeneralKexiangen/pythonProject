import requests
from bs4 import BeautifulSoup
import json
import pymysql
import time
from pyhive import hive


def get_appTableDatas():
    appTableDatas = []
    url = 'http://mingri-prod-simba-03:8088/cluster/apps/RUNNING'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
    re = requests.get(url, headers)
    re.encoding = re.apparent_encoding
    html = BeautifulSoup(re.text, 'html.parser')
    appsTableData = html.select('#apps > script')
    appsTableData = str(appsTableData).replace('[<script type="text/javascript">', '') \
        .replace('var appsTableData=', '') \
        .replace('</script>]', ' ').strip()
    appsTableData = json.loads(appsTableData)
    # print(appsTableData)
    # print(len(appsTableData))
    for appTableData in appsTableData:
        # print(appTableData)
        task_name = list(appTableData)[2]
        # print(task_name)
        if ('flink_' in str(list(appTableData)[2])):
            # print(list(appTableData)[-1])
            task_manager_data = list(appTableData)[-1].replace('<a href=\'', '').replace('\'>ApplicationMaster</a>', '')
            task_url = task_manager_data + 'taskmanagers'
            job_url = task_manager_data +'jobmanager/config'
            # print(task_manager_data)
            appTableDatas.append({'task_url': task_url, 'job_url': job_url, 'task_name': task_name})
    return appTableDatas


def get_info():
    infos = []
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent:': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    appTableDatas = get_appTableDatas()
    for appTableData in appTableDatas:
        task_url = appTableData.get('task_url')
        job_url = appTableData.get('job_url')
        re = requests.get(task_url, headers)
        re = re.json()
        taskmanagers = re.get('taskmanagers')
        re_job = requests.get(job_url, headers)
        re_job = re_job.json()
        allocated_memory = None
        for rej in re_job:
            if 'taskmanager.memory.process.size' == rej.get('key'):
                allocated_memory = rej.get('value')
                break
        allocated_memory = str(allocated_memory)+'B'
        if len(taskmanagers) > 0:
            containerid = taskmanagers[0].get('id')
            info = task_url + '/' + containerid
            result = requests.get(info, headers)
            result = result.json()
            metrics = result.get('metrics')
            metrics.update({'allocated_memory':allocated_memory})
            task_name = appTableData.get('task_name')
            task_info = json.dumps(metrics)
            print(task_name, task_info)
            infos.append({'task_name': task_name, 'task_info': task_info,
                          'crawl_time': str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))})
    return infos


def insert_data():
    # 连接hive
    hive_conn = hive.Connection(host='mingri-prod-simba-02', auth='CUSTOM', port=10000, username='hive',
                                password='hive', database='default')
    print('Connect hive success!')
    hive_cur = hive_conn.cursor()
    # 连接mysql
    mysql_conn = pymysql.connect(host='10.10.189.45', port=3306, user='USER_ONE', password='123456', db='dcresult',
                                 charset='utf8')
    print('Connect mysql success!')
    mysql_cur = mysql_conn.cursor()

    tn = 'stg_flink_task_info_crawl'

    infos = get_info()
    for info in infos:
        try:
            sql = '''insert into stg_flink_task_info_crawl (task_name,task_info,crawl_time) values (%s,%s,%s) '''
            param = ((str(info.get('task_name')), str(info.get('task_info')), str(info.get('crawl_time'))))
            # sql = '''insert into {0} partition(ds ='${yyyyMMdd}') values ('{1},'{2}','{3}') '''.format(tn,task_name,task_info,str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            print('执行sql语句：{0}'.format(sql))
            #mysql_cur.execute(sql, param)
        except Exception as e:
            print(e)
            return

    mysql_conn.commit()
    mysql_cur.close()
    mysql_conn.close()
    # hive_cur.execute(sql)
    # hive_cur.close()
    # hive_conn.close()


if __name__ == '__main__':
    insert_data()