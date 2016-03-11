# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from flask.ext import restful
from flask.ext.restful import Resource, Api,reqparse
import json
import time
import re

import mysql_deal
import rgb_deal

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#引自：http://blog.sina.com.cn/s/blog_6c39196501013s5b.html

app = Flask(__name__)
api = restful.Api(app)# 生成

parser = reqparse.RequestParser()
parser.add_argument('commodityid', type=str, help='我也不知道说啥')
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
        commodity = args["commodityid"]

        print(commodity)

        self.mysqlDeal = mysql_deal.MysqlDeal()
        #字符串解析
        
        datas["CommodityIDList"]= commodity
        dataL = commodity.split(",") # 字符串切分
        dataL.sort(key = int) # 按照int方式 进行排序
        data = ','.join(dataL) # 字符串拼接

        #调用数据库链接，添加数据
        r = self.mysqlDeal.all_deal("insert_removesuit",data)
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

        self.mysqlDeal = mysql_deal.MysqlDeal()

        #商品唯一性判断
        try:
            data = {}
            data["Name"] = "TaobaoID"
            data["Value"] = re.search(RTaobaoID, args_commodity["CommodityURL"]).group("TaobaoID")
            TaobaoID = str(data["Value"])
            HaveCommodityID = self.mysqlDeal.all_deal("select_commodity", data)
            if HaveCommodityID == ():
                pass
            elif HaveCommodityID[0].get("CommodityID") >= 0:
                return "商品的淘宝ID重复，已经存在的商品ID为："+str(HaveCommodityID[0].get("CommodityID"))
        except Exception as e:
            return "数据库链接错误"+e


        commodity_sql_f = ""
        commodity_sql_l = ""

        #添加至数据库
        for i in args_commodity:
            Pvalue = str(args_commodity.get(i))
            if i != "CommodityID":
                if i == "TaobaoID":
                    Pvalue = TaobaoID
                commodity_sql_f = commodity_sql_f + "`" + i + "`,"
                commodity_sql_l = commodity_sql_l + "'" + Pvalue + "',"

        commodity_sql = "INSERT INTO `commodity` ("+commodity_sql_f.rstrip(",")+") VALUES ("+commodity_sql_l.rstrip(",")+")"

        insert_commodityID = self.mysqlDeal.all_deal("insert_commodity", commodity_sql)

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
                self.rgb_deal = rgb_deal.RGBDeal()
                lsdata = DataDeal.DotDeal(args_commodityparameter.get(i))
                for edata in lsdata:
                    if "#" in edata:
                        edata = self.rgb_deal.HTMLColorToPILColor(edata)#颜色转换
                    qw = (str(i), int(edata), 10, int(insert_commodityID))
                    list_cpf.append(qw)
            list_cp.extend(list_cpf)

        insert_commodity_parameter = self.mysqlDeal.all_deal("insert_commodityparameter",list_cp)
        # print(insert_commodity_parameter)

        return {"CommodityID": insert_commodityID, "InsertCount": insert_commodity_parameter}

class DeleteCommodity(restful.Resource):

    def post(self):
        args = parser.parse_args()
        CommodityID = args["commodityid"]

        self.mysqlDeal = mysql_deal.MysqlDeal()
        #查询是否存在
        data = {}
        data["Name"] = "CommodityID"
        data["Value"] = CommodityID
        IsTrue = self.mysqlDeal.all_deal("select_commodity", data)

        if IsTrue == ():
            return "CommodityID不存在"

        #更改Commodity表状态
        IsDelete = self.mysqlDeal.all_deal("delete_commodity", CommodityID)

        if IsDelete == -1:
            return "Commodity表处理失败"
        elif IsDelete == 0:
            return "Commodity表没有改变，可能是该商品之前已经删除了"


        #删除CommodityParamter表内容
        IsDelete_CP = self.mysqlDeal.all_deal("delete_commodityparameter", CommodityID)
        if IsDelete_CP == 0:
            return "CommodityParameter表中不存在该CommodityID的商品"
        elif IsDelete_CP == -1:
            return "CommodityParameter表删除失败"

        #返回状态
        return "删除成功，共删除%s条。" % IsDelete_CP


class UpdateCommodity(restful.Resource):
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



        self.mysqlDeal = mysql_deal.MysqlDeal()

        #查看是否存在
        data = {}
        data["Name"] = "CommodityID"
        data["Value"] = args_commodity["CommodityID"]
        IsTrue = self.mysqlDeal.all_deal("select_commodity", data)

        if IsTrue == ():
            return "CommodityID不存在"


        sqlf = ""
        for i in args_commodity:
            Cvalue = str(args_commodity.get(i))
            if args_commodity.get(i) == "":
                pass
            if i == "CommodityID":
                pass
            else:
                if i == "TaobaoID":
                    Cvalue = re.search(RTaobaoID, args_commodity["CommodityURL"]).group("TaobaoID")
                sqlf = sqlf +"`"+ i +"`='"+Cvalue+"',"



        #更新Commodity表内容，主要的
        sql = "UPDATE `commodity` SET "+ sqlf.rstrip(",") +" WHERE (`CommodityID`=%s)" % args_commodity["CommodityID"]

        Update_Commodity = self.mysqlDeal.all_deal("update_commodity", sql)

        if Update_Commodity == -1:
            return "更新Commodity表失败"

        #删除CommodityParamter表内容
        IsDelete_CP = self.mysqlDeal.all_deal("delete_commodityparameter", args_commodity["CommodityID"])
        if IsDelete_CP == 0:
            return "CommodityParameter表中不存在该CommodityID的商品"
        elif IsDelete_CP == -1:
            return "CommodityParameter表删除失败"


        #取Json中的数据，添加CommodityParamter表内容
        list_cp = []
        for i in args_commodityparameter:
            list_cpf = []
            if args_commodityparameter.get(i) is "":
                pass
            else:
                self.rgb_deal = rgb_deal.RGBDeal()
                lsdata = DataDeal.DotDeal(args_commodityparameter.get(i))
                for edata in lsdata:
                    if "#" in edata:
                        edata = self.rgb_deal.HTMLColorToPILColor(edata)#颜色转换
                    qw = (str(i), int(edata), 10, int(args_commodity["CommodityID"]))
                    list_cpf.append(qw)
            list_cp.extend(list_cpf)

        insert_commodity_parameter = self.mysqlDeal.all_deal("insert_commodityparameter",list_cp)
        print("共添加%s个商品参数" % insert_commodity_parameter)

        return "修改成功"

class SelectCommodity(restful.Resource):
   def post(self):
        try:
            args = parser.parse_args()
            CommodityID = int(args["commodityid"])
        except:
            return "输入的参数错误，不为数字"


        self.mysqlDeal = mysql_deal.MysqlDeal()
        #查询是否存在
        data = {}
        data["Name"] = "CommodityID"
        data["Value"] = CommodityID
        Commodity_Info = self.mysqlDeal.all_deal("select_commodity", data)


        if Commodity_Info == ():
            return "CommodityID不存在"
        elif Commodity_Info == -1:
            return "查询Commodity表出错"


        CParamte_Info = self.mysqlDeal.all_deal("select_commodityparameter", data)

        if CParamte_Info == ():
            return "commodityparameter表中CommodityID不存在"
        elif CParamte_Info == -1:
            return "查询commodityparameter表出错"

        self.rgb_deal = rgb_deal.RGBDeal()
        CP_Data = {}
        #处理参数表内容
        try:
            for j in CParamte_Info:
                #颜色处理
                print(j)
                CPvalue = j.get("CPValueID")
                if "色盘" in j.get("CPName"):
                    CPvalue = self.rgb_deal.PILColorToHTMLColor(CPvalue)

                if CP_Data.get(j.get("CPName")) is None:
                    CP_Data[j.get("CPName")] = str(CPvalue)
                else:
                    CP_Data[j.get("CPName")] = str(CP_Data.get(j.get("CPName"))) +","+ str(CPvalue)
                print(CP_Data[j.get("CPName")])
        except Exception as e:
            print(e)

        print(type(Commodity_Info))
        print(type(CP_Data))
        return {"data": {"商品信息": Commodity_Info[0], "商品参数": CP_Data}}

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

api.add_resource(HelloWorld, '/') # 设定路由
api.add_resource(GetCommdityID, '/api/commodity') # 设定路由
api.add_resource(GetWeb, '/getweb') # 设定路由
api.add_resource(InsertCommodity, '/api/add') # 设定路由
api.add_resource(DeleteCommodity, '/api/del') # 设定路由
api.add_resource(UpdateCommodity, '/api/upd') # 设定路由
api.add_resource(SelectCommodity, '/api/sel') # 设定路由

if __name__ == '__main__':
    #app.run(debug=True)

    app.run(host='123.56.249.33', port=86)
