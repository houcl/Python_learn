# -*- coding: utf-8 -*-
import pymysql.cursors

connection = pymysql.connect(host='123.56.141.251',
                             user='root',
                             password='',
                             db='dadiao',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

class MysqlDeal(object):

    def insert_(self,data):
        if data is None:
            return
        #数据处理
        connection.commit()

        print(data)

        with connection.cursor() as cursor:
            #sql = "INSERT INTO `removesingle` (`CommodityIDList`) VALUES (%s)"
            sql = "INSERT INTO `dadiao`.`removesuit` (`CommodityIDList`) VALUES (%s);"
            try:
                r = cursor.execute(sql,data)
                return r
            except Exception as r:
                return r
            
            connection.close()
            
