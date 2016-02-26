# -*- coding: utf-8 -*-
import time
import re

datas = {}


class Uber_EveryDay(object):
    def regex_(self,source_html):
        RUGName = "<br/>用户组：(?P<UGName>.+?)（"
        RInTime = "（适用于(?P<InTime>.+?日)）<br/>"
        RArea = "【优步(?P<Area>[^<]+?)奖励政策】"
        RRewardContent = "<img src=\"(?P<RewardContent>[^（]+?)\" style"
        RBest = "获得任何奖励的前提条件：.+?\\*(?P<Best>.+?)<"
        
        datas["UGName"] = re.search(RUGName, source_html).group('UGName')
        datas["InTime"] = re.search(RInTime, source_html).group("InTime")
        datas["UGArea"] = re.search(RArea, source_html).group("Area")
        datas["RewardContent"] = re.search(RRewardContent, source_html).group("RewardContent")
        datas["InBest"] = re.search(RBest, source_html).group("Best")
        datas["Table"] = "group"
        datas["CreateTime"] =int(time.time())

        return datas



if __name__ == "__main__":
    my_regex = Uber_EveryDay()
    source_html = "姓名：王亮亮<br/>用户组：高端系列（适用于2月26日）<br/>奖励政策：<div><p><span style=\"color: rgb(66, 66, 66); font-weight: bold; line-height: 23.3333px;\">【优步北京奖励政策】</span><br></p></div><div><span style=\"color: rgb(66, 66, 66); line-height: 23.3333px; font-weight: bold;\">== 奖励政策 ==</span></div><div><span style=\"line-height: 23.3333px; color: rgb(255, 0, 0); font-weight: bold;\">获得任何奖励的前提条件：</span></div><div><span style=\"line-height: 23.3333px; color: inherit; font-weight: bold;\">*高端系列：当周评分的平均分高于4.8分，当周成单率高于65%，且当周完成至少10单（含10单）</span></div><div><span style=\"color: rgb(66, 66, 66); line-height: 23.3333px; font-weight: bold;\">如果您满足以上条件，会获得以下奖励：</span></div><div><span style=\"color: rgb(66, 66, 66); line-height: 23.3333px; font-weight: bold;\">== A. 高峰翻倍奖励 &amp; </span><span style=\"color: rgb(66, 66, 66); font-weight: bold; line-height: 23.3333px;\">每日成单奖励&nbsp;</span><span style=\"color: rgb(66, 66, 66); font-weight: bold; line-height: 23.3333px;\">==</span></div><div></div><div></div><div><img src=\"http://ac-jr33ks0c.clouddn.com/hxGKbqaV39WQiORbr0kaezrTukwDg6LTRRaFVixF.jpg\" style=\"width: 556px;\" id=\"exifviewer-img-2\" exifid=\"-1246503696\" oldsrc=\"http://ac-jr33ks0c.clouddn.com/hxGKbqaV39WQiORbr0kaezrTukwDg6LTRRaFVixF.jpg\"><br></div><div><p><span style=\"font-weight: bold; line-height: 1.5;\">== B.金牌服务奖励 ==</span><br></p><p><span style=\"color: rgb(255, 0, 0); font-weight: bold; line-height: 1.5;\">金牌车主服务奖励的前提条件需要满足：当周</span><span style=\"color: rgb(255, 0, 0); font-weight: bold; line-height: 1.5;\">成单率在75%以上、当周评分的平均分在4.8分以上</span></p><p><span style=\"font-weight: bold;\">a.达到该奖励前提，每周完成订单数最多的前300名合作车主可获得1300元金牌服务奖励；</span></p><p><span style=\"font-weight: bold;\">b.达到该奖励前提，每周完成订单数最多的前301-800名合作车主可获得1000元金牌服务奖励</span></p></div><div><span style=\"color: rgb(66, 66, 66); line-height: 23.3333px; font-weight: bold;\"><br></span></div><div><span style=\"line-height: 23.3333px; color: rgb(255, 0, 0); font-weight: bold;\">再次强调，获得以上任意奖励的前提条件是：</span></div><div><span style=\"color: rgb(66, 66, 66); line-height: 23.3333px; font-weight: bold;\">*高端系列：当周评分的平均分高于4.8分，当周成单率高于65%，且当周完成至少10个行程（含10个行程）</span></div><br/><br/>"
    datas =  my_regex.regex_(source_html)
    
    print(datas["UGName"])
    print("ok")
