# -*- coding: utf-8 -*-

import requests
import json
import re
import mssql_deal
import uber_everyday_info_regex
import time

datas = {}

import logging

ISOTIMEFORMAT='%Y_%m_%d'

logging.basicConfig(level = logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename="uber_msg_"+str(time.strftime(ISOTIMEFORMAT))+".log",
                    datefmt='%Y %b %d %H:%M:%S',
                    filemode='a'
                    )


#高端组
uber_every_mobile_data = {"phone":"13911020483","_ApplicationId":"jr33ks0cxx959koggypfvdaenvrv1ir0jtv4q37qwuzes8s4","_ApplicationKey":"jql3k3dgaerg4dsa81tntklw07pz4hb4yg1s2thmxxa0ty0v","_ClientVersion":"js0.5.1","_InstallationId":"ea974bce-e9e6-9df7-31ba-d1a3e85a06e8","_SessionToken":"oxim2j6ypurh7p8gzom0i5zx1"}
uber_every_mobile_url = "https://cn.avoscloud.com/1.1/functions/mobile_querCompanyGroup"


uber_every_company_url = "https://cn.avoscloud.com/1.1/functions/queryMobileGroup"
uber_every_company_data = {"objectId":"5668e57400b0023cfc166887","_ApplicationId":"jr33ks0cxx959koggypfvdaenvrv1ir0jtv4q37qwuzes8s4","_ApplicationKey":"jql3k3dgaerg4dsa81tntklw07pz4hb4yg1s2thmxxa0ty0v","_ClientVersion":"js0.5.1","_InstallationId":"ea974bce-e9e6-9df7-31ba-d1a3e85a06e8","_SessionToken":"oxim2j6ypurh7p8gzom0i5zx1"}



uber_every_headers = {
    "Content-Type": "text/plain", 
    "Host": "cn.avoscloud.com",
    "Connection": "Keep-Alive",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Origin":"http://uberbj.avosapps.com",
    "Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control":"no-cache" 
    }

try:
    uber_mobile_html = requests.post(uber_every_mobile_url, data=json.dumps(uber_every_mobile_data),headers=uber_every_headers,verify=False)

    uber_mobile_html_json = json.loads(uber_mobile_html.text)["result"]
    logging.info("高端获取的数据"+uber_mobile_html_json)
    #类初始化
    my_regex = uber_everyday_info_regex.Uber_EveryDay()
    datas = my_regex.regex_(uber_mobile_html_json)#添加数据，获取结果


    mssql = mssql_deal.MSsqlDeal()
        
    insert_data_state = mssql.insert_(datas)
    logging.info("高端处理结果"+insert_data_state)

    #获取电动车组的数据
    uber_company_html =requests.post(uber_every_company_url, data=json.dumps(uber_every_company_data),headers=uber_every_headers,verify=False)

    uber_company_html_json = json.loads(uber_company_html.text)["result"]
    logging.info("电动车获取的数据"+uber_company_html_json)

    datas = my_regex.regex_(uber_company_html_json)#添加数据，获取结果

    insert_data_state = mssql.insert_(datas)
    logging.info("电动车处理结果"+insert_data_state)



except ZeroDivisionError as e:
    logging.error(e)
    print('except:', e)
