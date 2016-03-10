# -*- coding: utf-8 -*-
import pymysql.cursors

# connection = pymysql.connect(host='123.56.141.251',
#                              user='root',
#                              password='',
#                              db='dadiao_d0309',
#                              charset='utf8',
#                              cursorclass=pymysql.cursors.DictCursor)


class MysqlDeal(object):
    conn = None


    def all_deal(self, howway, data):
        connection = pymysql.connect(host='123.56.141.251',
                             user='root',
                             password='',
                             db='dadiao_d0309',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

        self.conn = connection

        if howway is "insert_removesuit":
            return self.insert_removesuit(data)
        elif howway is "insert_commodity":
            return self.insert_commodity(data)
        elif howway is "select_commodity":
            return self.select_commodity(data)
        elif howway is "delete_commodity":
            return self.delete_commodity(data)
        elif howway is "update_commodity":
            return self.update_commodity(data)
        elif howway is "insert_commodityparameter":
            return self.insert_commodityparameter(data)
        elif howway is "delete_commodityparameter":
            return self.delete_commodityparameter(data)
        elif howway is "select_commodityparameter":
            return self.select_commodityparameter(data)

        connection.close()

    def insert_removesuit(self, data):
        if data is None:
            return

        print(data)

        with self.conn.cursor() as cursor:
            #sql = "INSERT INTO `removesingle` (`CommodityIDList`) VALUES (%s)"
            sql = u"INSERT INTO `dadiao`.`removesuit` (`CommodityIDList`) VALUES (%s);"
            try:
                cursor.execute(sql,data)
                connection.commit()
                return cursor.rowcount
            except Exception as r:
                return r

    def insert_commodity(self,data):
        if data is None:
            return
        #数据处理
        with self.conn.cursor() as cursor:
            sql = u"INSERT INTO `commodity` (`CategoryID`, `CommodityName`, `CommodityByname`, `CommodityURL`, `Operation`, `TaobaoID`, `OpenIID`, `PicURL`, `Price`, `Delete`, `OffShelf`, `PStatus`, `CreateTime`, `CollectNum`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            try:
                r = cursor.execute(sql, (data["CategoryID"], data["CommodityName"], data["CommodityByname"], data["CommodityURL"], data["Operation"], data["TaobaoID"], data["OpenIID"], data["PicURL"], data["Price"], data["Delete"], data["OffShelf"], data["PStatus"], data["CreateTime"], data["CollectNum"]))
                self.conn.commit()
                print(r)
                result = cursor.lastrowid #生成的ID

                return result
            except Exception as r:
                return r

    def select_commodity(self,data):
        if data is None:
            return
        #数据处理

        try:
            sql = "SELECT * FROM `commodity` WHERE %s = %s" % (data["Name"], data["Value"])
            cursor = self.conn.cursor()
            cursor.execute(sql)
            k = cursor.fetchall()
            cursor.close()
            return k
        except Exception as e:
            return e

    def insert_commodityparameter(self, data):
        if data is None:
            return

        try:
            cursor = self.conn.cursor()
            sql = u"INSERT INTO `commodityparameter` (`CPName`, `CPValueID`, `Score`, `CommodityID`) VALUES (%s, %s, %s, %s)"
            # for i in data:
            #     cursor.execute(sql, (i.get("CPName"), i.get("CPValueID"), i.get("Score"), i.get("CommodityID")))
            cursor.executemany(sql, data)
            self.conn.commit()
            cursor.close()
            return cursor.rowcount

        except Exception as e:
            self.conn.rollback()
            return e

    #此处为物理删除
    def delete_commodityparameter(self, data):
        if data is None:
            return

        try:
            cursor = self.conn.cursor()
            sql = u"DELETE FROM `commodityparameter` WHERE CommodityID = %s" % data

            cursor.execute(sql)

            self.conn.commit()
            cursor.close()
            return cursor.rowcount

        except Exception as e:
            self.conn.rollback()
            print(e)
            return -1

    def select_commodityparameter(self, data):
        if data is None:
            return

        try:
            cursor = self.conn.cursor()
            sql = u"SELECT CPName,CPValueID FROM `commodityparameter` WHERE %s = %s" % (data["Name"], data["Value"])

            cursor.execute(sql)

            self.conn.commit()
            cursor.close()
            return cursor.fetchall()

        except Exception as e:
            self.conn.rollback()
            print(e)
            return -1


    def delete_commodity(self, data):
        with self.conn.cursor() as cursor:
            sql = u"UPDATE `commodity` SET  `Delete`='1' WHERE (`CommodityID`= %s);"
            try:
                r = cursor.execute(sql, data)
                self.conn.commit()
                return r
            except Exception as r:
                print(r)
                return -1


    def update_commodity(self, data):
        with self.conn.cursor() as cursor:
            sql = data
            try:
                r = cursor.execute(sql)
                self.conn.commit()
                return r
            except Exception as r:
                print(r)
                return -1
