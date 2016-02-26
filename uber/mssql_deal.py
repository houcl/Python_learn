# -*- coding:utf-8 -*-
import pyodbc


connection = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=qds185861603.my3w.com;port=1433;DATABASE=qds185861603_db;UID=qds185861603;PWD=qwer1234;TDS_Version=8.0;')
    #'DRIVER={SQL Server};SERVER=qds185861603.my3w.com;DATABASE=qds185861603_db;UID=qds185861603;PWD=qwer1234')
	
class MSsqlDeal(object):

    def select_(self,datas):
        #数据处理
        #connection.commit()
        
        #print(data)

        with connection.cursor() as cursor:
            #sql = "INSERT INTO `removesingle` (`CommodityIDList`) VALUES (%s)"
            #sql = "SELECT * FROM [dbo].[uber_msg] WHERE UMsgID = ?"
            sql = ""
            data = ""
            if datas["Table"] == "msg":
                sql = "SELECT * FROM [dbo].[uber_msg] WHERE ObjectID = ?"
                data = datas["ObjectID"]
            elif datas["Table"] == "group":
                sql = "SELECT * FROM [dbo].[uber_group_info] WHERE RewardContent = ?"
                data = datas["RewardContent"]
            
            try:
                r = cursor.execute(sql,data).fetchall()
                print(r)
                if r is None:
                    return 0
                else :
                    return 1

            except Exception as r:
                print(r)
                return r
            
            connection.close()

    # 定义插入数据库
    def insert_(self,datas):
        if datas is None:
            return
        
        with connection.cursor() as cursor:
            #sql = "INSERT INTO `removesingle` (`CommodityIDList`) VALUES (%s)"
            #sql = "SELECT * FROM [dbo].[uber_msg] WHERE UMsgID = ?"
            sql = ""
            data = ""
            
            if datas["Table"] == "msg":
                sql = ("INSERT INTO [dbo].[uber_msg] "
                       "([ObjectID], [Title], [TopNews], [MsgRead], [SendTime], [UCreatedAt], [UUpdatedAt], [CreateTime], [UpdateTime], [PicUrl])"
                       "VALUES (?,?,?,?,?,?,?,?,?,?)")
                data = (datas["ObjectID"],datas["Title"],datas["TopNews"],datas["MsgRead"],datas["SendTime"],datas["UCreatedAt"],datas["UUpdatedAt"],datas["CreateTime"],datas["UpdateTime"],datas["PicUrl"])

            elif datas["Table"] == "group":
                sql = ("INSERT INTO [dbo].[uber_group_info] "
                       "([UGName], [UGArea], [RewardContent], [InTime], [InBest], [CreateTime]) "
                       "VALUES (?,?,?,?,?,?)")
                data = (datas["UGName"],datas["UGArea"],datas["RewardContent"],datas["InTime"],datas["InBest"],datas["CreateTime"])
            try:
                r = cursor.execute(sql,data)

                print(cursor.rowcount)#受影响行数
                
                return r
            except Exception as r:
                print(r)

                return cursor.rowcount
            
            connection.close()



         # main函数
if __name__ == "__main__":
    # 定义入口
    
    obj_spider = MSsqlDeal()
##    obj_spider.select_(1)

    datas = {}

    datas["Title"] = "励政策已更新"
    datas["ObjectID"] = "56c34a21a633bd1154b169a8"
    datas["TopNews"] = 1
    datas["MsgRead"] = "msgRead"
    datas["SendTime"] = "msgRead"
    datas["UCreatedAt"] = "2016"
    datas["UUpdatedAt"] = "20168"
    datas["PicUrl"] = "ceshi"
    datas[""]

    q = obj_spider.insert_(datas)
    print(q)

    
