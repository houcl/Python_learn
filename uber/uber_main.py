# -*- coding: utf-8 -*-
import requests
import json
import mssql_deal
import time
from bs4 import BeautifulSoup

import logging

ISOTIMEFORMAT='%Y_%m_%d'

logging.basicConfig(level = logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename="uber_msg_"+str(time.strftime(ISOTIMEFORMAT))+".log",
                    datefmt='%Y %b %d %H:%M:%S',
                    filemode='a'
                    )

uber_msg_headers = {
    "Content-Type": "text/plain", 
    "Host": "cn.avoscloud.com",
    "Expect": "100-continue",
    "Connection": "Keep-Alive",
    "User-Agent":""
    }

datas = {}

# 定义请求的数据内容
uber_msg_data = {"username":"15222226292","pageNo":1,"pageSize":10,"_ApplicationId":"jr33ks0cxx959koggypfvdaenvrv1ir0jtv4q37qwuzes8s4","_ApplicationKey":"jql3k3dgaerg4dsa81tntklw07pz4hb4yg1s2thmxxa0ty0v","_ClientVersion":"js0.5.1","_InstallationId":"b5eea16b-e31a-49d1-ecc2-ddb88c0fdc46","_SessionToken":"oxim2j6ypurh7p8gzom0i5zx1"}

uber_msg_url = "https://cn.avoscloud.com/1.1/functions/mobile_getMsg"



try:
    r = requests.post(uber_msg_url, data=json.dumps(uber_msg_data),headers=uber_msg_headers, verify=False)
    print(r.text)
    logging.info(r.text)
    #json 解析
    r = json.loads(r.text)
    jsonlistL = r["result"]

    for jsonv in jsonlistL:
        datas["Title"] = jsonv["title"]
        datas["ObjectID"] = jsonv["objectId"]
        datas["TopNews"] = jsonv["topNews"]
        datas["MsgRead"] = jsonv["msgRead"]["className"]
        datas["SendTime"] = jsonv["sendTime"]["iso"]
        datas["UCreatedAt"] = jsonv["createdAt"]
        datas["UUpdatedAt"] = jsonv["updatedAt"]
        datas["UUpdatedAt"] = jsonv["updatedAt"]
        datas["CreateTime"] = int(time.time())
        datas["UpdateTime"] = int(time.time())
        datas["Table"] = "msg"
##
        # datas["ObjectID"] = "56c9514e2e958a0059100fd1"
        #发送请求获取图片内容
        uber_pic_headers = {
            "Content-Type": "text/plain", 
            "Host": "cn.avoscloud.com",
            "Connection": "Keep-Alive",
            "Referer":"http://uberbj.avosapps.com/mobile/msgdetail.html?msgid="+datas["ObjectID"],
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
            "Origin":"http://uberbj.avosapps.com",
            "Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control":"no-cache"
            
            }
        
        uber_pic_url = "https://cn.avoscloud.com/1.1/classes/msgPush/"+datas["ObjectID"]
        
        uber_pic_data={
                "where":
                {
                        "objectId":""+datas["ObjectID"]+""
                        },
                "limit":1,
                "_method":"GET",
                "_ApplicationId":"jr33ks0cxx959koggypfvdaenvrv1ir0jtv4q37qwuzes8s4",
                "_ApplicationKey":"jql3k3dgaerg4dsa81tntklw07pz4hb4yg1s2thmxxa0ty0v",
                "_ClientVersion":"js0.5.1",
                "_InstallationId":"b5eea16b-e31a-49d1-ecc2-ddb88c0fdc46",
                "_SessionToken":"oxim2j6ypurh7p8gzom0i5zx1"
                }
                
        
        uber_pic = requests.get(uber_pic_url, data=json.dumps(uber_pic_data),headers=uber_pic_headers, verify=False)
        print(uber_pic.text)
        uber_pic_json = json.loads(uber_pic.text)#转化成json
        logging.info(uber_pic_json)

        uber_pic_json_html = uber_pic_json["content"]#获取html内容

        soup =BeautifulSoup(uber_pic_json_html, 'html.parser', from_encoding='utf-8')

        uber_pic_url_content = ""
        try:
            uber_pic_url_content = soup.find("img").get("src")
        except:
            logging.info("该页没图")


        
        datas["PicUrl"] = uber_pic_url_content

        
        mssql = mssql_deal.MSsqlDeal()
        
        insert_data_state = mssql.insert_(datas)
        print(uber_pic_url)
        logging.info(insert_data_state)
        #print(insert_data_state)
        
    
    #print(r.text)

except ZeroDivisionError as e:
    logging.error(e)
    print('except:', e)
