# -*- coding: utf-8 -*-
import pymysql
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

con = pymysql.connect(host="192.168.89.172", user="root", password="1qaz%TGB", database="ads_nuza", charset="utf8")
c = con.cursor()
sql = '''select prod_code,prod_show_img_url from tmp_prod_picture where prod_show_img_url is not null'''
c.execute(sql)
con.commit()
res= c.fetchall()
urls ={}
for re in res:
    # urls.append(re[1])
    urls[re[0]] = re[1]
error_urls = []
i = 0
for key in urls.keys():
    if i > 100:
        break
    resp = requests.get(urls.get(key))
    try:
        image = Image.open(BytesIO(resp.content))
        # image.show()
        print(urls.get(key), image.size)
    except:
        error_urls.append(key)
    i+=1
    print('第{0}条url了'.format(str(i)))
print('>>>>>', pd.DataFrame(error_urls))
c.close()
con.close()
