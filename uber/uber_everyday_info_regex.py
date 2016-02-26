# -*- coding: utf-8 -*-
import time

datas = {}


class Uber_EveryDay(object):
    def regex_(self,source_html):
        RUGName = "<br/>用户组：(?P<UGName>.+?)（"
        RInTime = "（适用于(?P<InTime>.+?日)）<br/>"
        RArea = "【优步(?P<Area>[^<]+?)奖励政策】"
        RRewardContent = "<img src=\"(?P<RewardContent>[^（]+?)\" style"
        RBest = "获得任何奖励的前提条件：.+?\\*(?P<Best>.+?)<"
        datas["UGName"] = re.search(RUGName, source_html).group("UGName")
        datas["InTime"] = re.search(RInTime, source_html).group("InTime")
        datas["UGArea"] = re.search(RArea, source_html).group("Area")
        datas["RewardContent"] = re.search(RRewardContent, source_html).group("RewardContent")
        datas["InBest"] = re.search(RBest, source_html).group("Best")
        datas["Table"] = "group"
        datas["CreateTime"] =int(time.time())

        return datas
