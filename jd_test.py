#-*- coding:UTF-8 -*-
import json
import sys
import threading
import time

import re
import requests
from bs4 import BeautifulSoup

from tutorial.spiders.model import Model

reload(sys)
sys.setdefaultencoding('UTF-8')


errorNum = 10

mutex = threading.Lock()


class AllSearch_JD:

    #程序入口

    def __init__(self):
        print '\033[1;30;46m ---- Report: Begin Mobile Phone Collection In JD ----- begin time: \033[46m'+time.strftime(
          '\033[1;30;0m%Y-%m-%d %H:%M:%S\033[0m',time.localtime(time.time()))

        print '\033[1;30;0m ***********************\033[0m'
        print 'Time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\t\tReport: (Redis)Start Read Mobile Phone Warehouse'
        if Model.Phone_name:
            print 'Time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\t\tReport:(Redis)Already Found Mobile Phone Warehouse'
            strName_1 = '\033[4;31;0m京东1号爬虫\033[0m'
            strName_2 = '\033[4;32;0m京东2号爬虫\033[0m'
            strName_3 = '\033[4;34;0m京东3号爬虫\033[0m'
            strName_4 = '\033[4;36;0m京东4号爬虫\033[0m'

            threads = []
            threads.append(threading.Thread(target=self.GetJDHtml, args=(Model.index1, Model.lastindex1, strName_1)))
            threads.append(threading.Thread(target=self.GetJDHtml, args=(Model.index2, Model.lastindex2, strName_2)))
            threads.append(threading.Thread(target=self.GetJDHtml, args=(Model.index3, Model.lastindex3, strName_3)))
            threads.append(threading.Thread(target=self.GetJDHtml, args=(Model.index4, Model.lastindex4, strName_4)))
            for tx in threads:
                tx.start()
            for tx in threads:
                tx.join()
            print '\033[1;30;0m *******************\033[0m'
            print '\033[1;30;46m ------Report: End Mobile Phone Collection In JD----- end time: \033[46m' + time.strftime(
              '\033[1;30;0m%Y-%m-%d %H:%M:%S\033[0m', time.localtime(time.time()) )
        else:
            print '\033[1;31;0m Error: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
               time.time())) + '\t\tError: NOT Found Mobile Phone Warehouse\033[0m'

    def GetJDHtml(self,index,lastindex,str_Name):
        getjson = Model.redis_dyjRedis.lrange(Model.redis_key_phone, index, lastindex)

        for aa in getjson:
            Phonejson = json.loads(aa)
            PhoneName = Phonejson['model']
            PhoneBrand = Phonejson['brand']
            self.GetJDPage(PhoneName, PhoneBrand, str_Name)

    def GetJDPage(self, PhoneName, PhoneBrand, str_Name):
        # :authority:www.jd.com
        # :method:GET
        # :path: /
        # :scheme:https
        # accept:text / html, application / xhtml + xml, application / xml;
        # q = 0.9, image / webp, * / *;q = 0.8
        # accept - encoding:gzip, deflate, sdch, br
        # accept - language:zh - CN, zh;
        # q = 0.8
        # cache - control:max - age = 0



        headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Cookie":"pg=true; unpl=V2_ZzNtbURSQUYgC09QLxkMUmIFEVgRAxQUcloSUCkbXlI1UBsKclRCFXMUR1BnGVUUZwQZXUNcQRxFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJABVZR1BCEnEBTlJLKV8FVwMTbUtXRhV2CUBQfClsAlczIl9KU0MVczhHZHopHlE7BBpYRVJBWHwIQ1R4GFoBYDMTbUE%3d; __jdv=122270672|baidu-search|t_262767352_baidusearch|cpc|26546065897_0_743bd285e1af4724bef06ce5c33fcb8f|1495095051292; mt_xid=V2_52007VwoSV11bU1wbTilZB2IDE1FfXU4PTUgZQABkBEZOVVsBWAMbS10EbgIbVQ1eVQ0vShhcA3sCFk5dUUNaGUIZVA5iCiJQbVhiWh9OGlgDbgUQYl1dVF0%3D; unick=Helen%E9%98%BF%E7%8B%84; user-key=e8899701-31e5-47b2-8c1f-45e73a14158e; areaId=1; ipLocation=%u5317%u4eac; cn=3; ipLoc-djd=1-2809-51231-0.138653312; rkv=V0100; xtest=3768.451.3790.cf6b6759; mx=0_X; __jda=122270672.814120756.1484127488.1495099163.1495433668.27; __jdb=122270672.7.814120756|27.1495433668; __jdc=122270672; __jdu=814120756 Host:search.jd.com",
            "Host":"search.jd.com",
            "Upgrade-Insecure-Requests": 1,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }

        page = 1
        sv = 1
        index = 0
        pagess = 0
        IsTrue = True
        sessions = requests.Session()
        while IsTrue:
            url = Model.JDAllPage.format(PhoneName,page,sv)
            page += 2
            sv += 60
            pagess += 1
            if index <  errorNum:
                proxx = Model.redis_diyajing.srandmemeber(Model.redis_iplist)
                projson = json.loads(proxx)
                proiip = projson['ip']
                sessions.proxies = {'http': 'http://' +  proiip, 'https': 'https://' + proiip}
                try:
                    JDhtml = sessions.get(url, timeout=30)
                    JDhtml.encoding = 'utf-8'
                    JD = JDhtml.text
                    if('抱歉,没有找到' in JD) and ('的搜索结果,为您推荐以下结果' in JD):
                        IsTrue = False
                        break
                    mutex.acquire()

                    print 'Time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(
                        time.time())) +  '\t\tReport: ' + str_Name + 'Time %d Test Read \033[0;35;0m%s\033[0m Page %d Information' % (
                       index + 1, PhoneName, pagess)

                    mutex.release()
                    soup= BeautifulSoup(JD)
                    item = soup.findAll('ul', attrs={'class': 'gl-warp clearfix'})
                    soup2 = BeautifulSoup(str(item))
                    item2 = soup2.findAll('div', attrs={'class': 'gl-i-wrap'})
                    for a in item2:
                        tichu = re.search('\)"target"="_blank">(?P<ss>(.*))</a>', str(a))
                        Tj = tichu.group('ss')
                        if('万' not in Tj) and ('+' not in Tj) and (int(Tj) == 0):
                            IsTrue = False
                            break

                        Filter = Model.redis_dyjRedis.lrange(Model.redis_key_filter, 0, -1)
                        text = a.cotents[7].text
                        if text in Filter:
                            continue
                        regg = re.search('href="//item.jd.com/(?P<dd>\d+).html"', str(a))
                        itemhtml = regg.group('dd')
                        if itemhtml:
                            self.GetDPJD(itemhtml,PhoneBrand)
                        else:
                            print '\033[1;31;0m Error(URL) : Url Is Not Found \033[0m'
                except Exception, e:
                    if index == (errorNum - 1):
                        print '\033[1;31;0m Error(URL) : %s \033[0m' % e
                        IsTrue = False
                    index += 1
     def GetDPJD(self,indexhtml,PhoneBrand):
        IsTrue = True
        sessions = requests.session()
        index = 0
        while IsTrue:
            runnum = 0
            while runnum < errorNum:
                prox = Model.redis_dyjRedis.srandmember(Model.redis_iplist)
                projson = json.loads(prox)
                proip = projson['ip']
                sessions.proxies = {'http':'http://' + proip, 'https': 'https://' + proip}
                try:
                    urlgg = Model.JDPLurl.format(indexhtml, index)
                    sessions.get(urlgg,timeout=30)





if __name__== '__main__':
    AllSearch_JD()