from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from flask import Flask,request
import pymysql
import json


appGet = FastAPI()

@appGet.get('/test/a={a}/b={b}')
def calculate(a: int = None, b: int = None):
    c = a + b
    res = {"res": c}
    return res


appPost = FastAPI()

class Item(BaseModel):
    a: int = None
    b: int = None

@appPost.post('/test')
def calculate(request_data: Item):
    a = request_data.a
    b = request_data.b
    c = a + b
    res = {"res": c}
    return res

appFlask = Flask(__name__)

#@appFlask.route('/index',methods = ['POST'])
@appFlask.route('/index1', methods=['POST'])

def get_index():
    inputData = request.values.get("inputData")
    content = get_contents(inputData)
    return content

def get_contents(inputData):
    #连接mysql
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root1234', db='test', charset='utf8')
    cursor = conn.cursor()
    sql = "select name,age,sex,cellphone from students where name = '%s'"%(inputData)
    # sql = "select name,age,sex,cellphone from students"
    cursor.execute(sql)
    data = cursor.fetchone()
    print(data)
    result = {'name': data[0], 'age': data[1], 'sex': data[2], 'cellphone': data[3]}
    # datas = cursor.fetchall()
    # re = []
    # for data in datas:
    #     result = {'name': data[0], 'age': data[1], 'sex': data[2], 'cellphone': data[3]}
    #     re.append(result)
    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps(result, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # uvicorn.run(app=appPost,
    #             host="0.0.0.0",
    #             port=8080,
    #             workers=1)
    appFlask.run(host='0.0.0.0', port=5590)