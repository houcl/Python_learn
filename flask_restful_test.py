from flask import Flask, request, render_template
from flask.ext import restful
from flask.ext.restful import Resource, Api,reqparse

import mysql_deal

app = Flask(__name__)
api = restful.Api(app)# 生成

parser = reqparse.RequestParser()
parser.add_argument('commodiyt', type=str, help='我也不知道说啥')


datas = {}

class GetWeb(restful.Resource):
    def get(self):
        return render_template('/templates/commodity.html')

class HelloWorld(restful.Resource):
    def get(self): #实现了get方法
        qwe= "htllo world"
        return qwe

class GetCommdityID(restful.Resource):
    def get(self):
        args = parser.parse_args()
        commodiyt = args["commodiyt"]

        print(commodiyt)

        self.mysqlDeal = mysql_deal.MysqlDeal()
        #字符串解析
        
        datas["CommodityIDList"]= commodiyt
        dataL = commodiyt.split(",") # 字符串切分
        dataL.sort(key = int) # 按照int方式 进行排序
        data = ','.join(dataL) # 字符串拼接

        #调用数据库链接，添加数据
        r = self.mysqlDeal.insert_(data)
        rt = {"state":"%s"%r}

        return rt
    
    def post(self):
        args = parser.parse_args()
        self.mysqlDeal = mysql_deal.MysqlDeal()
        commodiyt = args["commodiyt"]
        #字符串解析
        
        datas["CommodityIDList"]= commodiyt
        dataL = commodiyt.split(",") # 字符串切分
        dataL.sort(key = int) # 按照int方式 进行排序
        data = ','.join(dataL) # 字符串拼接

        #调用数据库链接，添加数据
        r = self.mysqlDeal.insert_(data)
        rt = {"state":"%s"%r}

        return rt


api.add_resource(HelloWorld, '/') # 设定路由
api.add_resource(GetCommdityID, '/commodiyt') # 设定路由
api.add_resource(GetWeb, '/getweb') # 设定路由


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='123.56.249.33', port=8080)