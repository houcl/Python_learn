# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask.ext import restful
from flask.ext.restful import Resource, Api,reqparse
import json
import time
import re

import mysql_deal

app = Flask(__name__)
api = restful.Api(app)# 生成

parser = reqparse.RequestParser()
parser.add_argument('commodiyt', type=str, help='我也不知道说啥')
parser.add_argument('data', type=str, help='Rate to charge for this resource')

@app.route('/index')
def index():
    return render_template('/commodity.html')

datas = {}
commodity_info = {}


class GetWeb(restful.Resource):
    def get(self):
        return render_template('/commodity.html')

class HelloWorld(restful.Resource):
    def get(self): #实现了get方法
        qwe= "htllo world"
        return qwe

class GetCommdityID(restful.Resource):
    def get(self):
        args = parser.parse_args()
        commodity = args["commodiyt"]

        print(commodity)

        self.mysqlDeal = mysql_deal.MysqlDeal()
        #字符串解析
        
        datas["CommodityIDList"]= commodiyt
        dataL = commodiyt.split(",") # 字符串切分
        dataL.sort(key = int) # 按照int方式 进行排序
        data = ','.join(dataL) # 字符串拼接

        #调用数据库链接，添加数据
        r = self.mysqlDeal.all_deal(insert_removesuit,data)
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
        r = self.mysqlDeal.all_deal(insert_removesuit, data)
        rt = {"state":"%s"%r}

        return rt

class InsertCommodity(restful.Resource):
    def get(self):
        qwe= "hello world"
        return qwe

    def post(self):
        args = parser.parse_args()
        args_json = ""
        try:
            args_json = json.loads(args["data"].replace("'", "\""))#此处特殊注意，需要将获取到的json中的单引号，转化成双引号
        except Exception as e:
            print(e)

        RTaobaoID = "id=(?P<TaobaoID>\d+)"

        args_commodity = args_json["商品信息"]
        args_commodityparameter = args_json["商品参数"]


        #切出来商品信息
        commodity_info["CategoryID"] = args_commodity["CategoryID"]
        commodity_info["CommodityURL"] = args_commodity["CommodityURL"]
        commodity_info["Operation"] = args_commodity["Operation"]
        commodity_info["CreateTime"] = int(time.time())
        commodity_info["CommodityName"] = args_commodity["CommodityName"]
        commodity_info["CommodityByname"] = args_commodity["CommodityName"]
        commodity_info["TaobaoID"] = re.search(RTaobaoID, args_commodity["CommodityURL"]).group("TaobaoID") #特殊处理
        commodity_info["OpenIID"] = args_commodity["OpenIID"]
        commodity_info["PicURL"] = args_commodity["PicURL"]
        commodity_info["Price"] = args_commodity["Price"]
        commodity_info["Delete"] = 0
        commodity_info["OffShelf"] = args_commodity["OffShelf"]
        commodity_info["PStatus"] = args_commodity["PStatus"]
        commodity_info["CollectNum"] = 0

        self.mysqlDeal = mysql_deal.MysqlDeal()

        #商品唯一性判断
        try:
            HaveCommodityID = self.mysqlDeal.all_deal("select_commodity", commodity_info["TaobaoID"])
            if HaveCommodityID == 1:
                return "商品ID重复"
        except Exception as e:
            return "数据库链接错误"+e



        #添加至数据库
        insert_commodityID = self.mysqlDeal.all_deal("insert_commodity",commodity_info)
        rt = {"state":"%s" %insert_commodityID}
        print(rt)

        if insert_commodityID is None:
            return "添加商品失败"


        #添加商品参数

        #批量添加时存在些许问题
        #取Json中的数据
        list_cp = []
        for i in args_commodityparameter:
            list_cpf = []
            if args_commodityparameter.get(i) is "":
                pass
            else:

                lsdata = DataDeal.DotDeal(args_commodityparameter.get(i))
                for edata in lsdata:
                    if "#" in edata:
                        edata = DataDeal.HTMLColorToPILColor(edata)#颜色转换
                    #
                    # commodity_parameter = {}
                    # commodity_parameter["CPName"] = str(i)
                    # commodity_parameter["CPValueID"] = int(edata) #需要特殊处理
                    # commodity_parameter["Score"] = 10 # 之后可能会去掉
                    # commodity_parameter["CommodityID"] = 99999 #insert_commodityID
                    qw = (str(i), int(edata), 10, int(insert_commodityID))
                    list_cpf.append(qw)
            list_cp.extend(list_cpf)

        insert_commodity_parameter = self.mysqlDeal.all_deal("insert_commodityparameter",list_cp)
        print(insert_commodity_parameter)

        return insert_commodity_parameter


class DataDeal(object):
    #逗号分隔
    def DotDeal(data):
        if "," in data:
            lsdata = data.split(",")
            return lsdata
        else:
            lsdata = []
            lsdata.append(data)
            return lsdata

    #色彩转换
    def RGBToHTMLColor(rgb_tuple):
        """ convert an (R, G, B) tuple to #RRGGBB """

        hexcolor = '#%02x%02x%02x' % rgb_tuple

        # that's it! '%02x' means zero-padded, 2-digit hex values

        return hexcolor

    def HTMLColorToRGB(colorstring):
        """ convert #RRGGBB to an (R, G, B) tuple """

        colorstring = colorstring.strip()

        if colorstring[0] == '#': colorstring = colorstring[1:]

        if len(colorstring) != 6:
            return ValueError, "input #%s is not in #RRGGBB format" % colorstring

        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]

        return (r, g, b)

    def HTMLColorToPILColor(colorstring):
        """ converts #RRGGBB to PIL-compatible integers"""

        colorstring = colorstring.strip()

        while colorstring[0] == '#': colorstring = colorstring[1:]
        # get bytes in reverse order to deal with PIL quirk
        colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
        # finally, make it numeric
        color = int(colorstring, 16)

        return color

    def PILColorToRGB(pil_color):
        """ convert a PIL-compatible integer into an (r, g, b) tuple """
        hexstr = '%06x' % pil_color
        # reverse byte order
        r, g, b = hexstr[4:], hexstr[2:4], hexstr[:2]
        r, g, b = [int(n, 16) for n in (r, g, b)]

        return (r, g, b)

    def PILColorToHTMLColor(pil_integer):
        k = DataDeal.PILColorToRGB(pil_integer)
        q = DataDeal.RGBToHTMLColor(k)
        return q

    def RGBToPILColor(rgb_tuple):
        return HTMLColorToPILColor(RGBToHTMLColor(rgb_tuple))


api.add_resource(HelloWorld, '/') # 设定路由
api.add_resource(GetCommdityID, '/commodiyt') # 设定路由
api.add_resource(GetWeb, '/getweb') # 设定路由
api.add_resource(InsertCommodity, '/add') # 设定路由


if __name__ == '__main__':
    #app.run(debug=True)
    debug = True
    app.run(host='127.0.0.1', port=5009)
