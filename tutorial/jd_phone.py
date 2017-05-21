import json
import sys

import time

import re
import requests
from bs4 import BeautifulSoup

from tutorial.spiders.model import Model

reload(sys)
sys.setdefaultencoding('utf-8')


errorNum = 10

class FindToPhone:

    def __init__(self):
        print '\033[1;30;46m -----报告: 开始进行手机采集 --------- begin time:\033[46m' + time.strftime('\033[1;30;0m%Y-%m-%d %H:%M:%S\033[0m',time.localtime(time.time()))
        print '\033[1;30;0m *****************\033[0m'
        print ' Time: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\t\t报告:开始读取手机型号库'
        if Model.Phone_name:
            print ' Time:'+ time.strtime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) +'\t\t报告:已找到手机型号库'
        else:
            print '\033[5;31;0m Error : 没有找到手机型号 \033[0m'
        while True:
            aa = Model.redis_dyjRedis.lpop(Model.redis_key_phone)
            if aa:
                PhoneJson = json.loads(aa)
                PhoneName = PhoneJson['model']
                Brand = PhoneJson['brand']
            else:
                break


    def GetJDPhone(self,PhoneName,brand):
        index = 0
        isTrue = True
        urlgg = Model.JDSearch.format(PhoneName)
        sessons = requests.session()
        while isTrue :
            if index >= errorNum:
                print '\033[0;30;43m Time:' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()
                      ))+'\t\t\033[4;31;0m京东爬虫\033[0m报告: 获取\033[1;35;43m%s\033[43m的信息失败\033[0m' % PhoneName
                break

            proxy = Model.redis_dyjRedis.scrandmember(Model.redis_iplist)
            proxyjson = json.loads(proxy)
            proxiip = proxyjson['ip']
            sessons.proxies = {'http': 'http://' + proxiip, 'https':'https://'+proxiip}
            try:
                print 'Time: '+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\t\t\033[4;31;0m京东爬虫\033[0m京东爬虫\033[0m报告: 开始第%d次尝试读取\033[0;35;0m%s\033[0m销售信息' % (index + 1,PhoneName),
                JDhtml = sessons.get(urlgg, timeout=30)
                JDhtml.encoding = 'utf-8'
                JD = JDhtml.text
                self.GetJDInformation(JD, brand, PhoneName)
                print '\033[0;32;0m成功√\033[0m'
                isTrue = False
            except Exception, e:
                index += 1
                print '\033[0;31;0m失败×\033[0m'


    def GetJDInformation(self,html,brand,phonename):

        index = 0
        sessions = requests.session()
        soup = BeautifulSoup(html)
        items = soup.findAll('div', attrs={"class": "p-name p-name-type-2"})
        try:
            for i in items:
                isTrue = True
                NowRead = 1
                gg = re.search(r'href="//item.jd.com/(?P<dd>\d+).html"', str(i))
                Itemhtml = gg.group("dd")
                soupgg = BeautifulSoup(str(i))
                text = soupgg.text
            for a in Model.FilterName:
                if str(a) in text:
                    isTrue = False
                    break
            if isTrue:
                if index <  Model.AllNum:
                    urlJson = '{"attrs":{"category":"手机","brand":"%s","model":"%s","urlweb":"JD"},"url":"%s"}' % (
                    brand, phonename, Model.JDDPurl.format(Itemhtml))
                    Model.redis_dyjRedis.lpush(Model.redis_insert_url,urlJson)
                    while NowRead<errorNum:
                        proxy = Model.redis_dyjRedis.srandmember(Model.redis_iplist)
                        proxyjson = json.loads(proxy)
                        proxyiip = proxyjson["ip"]
                        sessions.proxies = {'http':'http://' + proxyiip, 'https': 'https://'+proxyiip}
                        try:
                            JDDPhtml = sessions.get(Model.JDDPurl.format(Itemhtml), timeout=30)
                            JDDPhtml.encoding = 'utf-8'
                            JDDPht = JDDPhtml.text
                            if JDDPht:
                                DPSoup = BeautifulSoup(JDDPht)
                                div_text = DPSoup.findAll('div', attrs={'class': 'Ptable'})
                                '{"attrs":{"category":"phone","brand":"%s","model":"%s","buyer_name":"%s","seller_name":"%s","pl":"%s","pl_time":"%s","color":"%s",'\
                                '"network_type":"%s","memory":"%s","buy_type":"%s","version":"%s","urlweb","%s"}}'

                                index += 1
                                break
                            else:
                                print 'JD Web cannot read anything!'
                        except Exception, e:



        except

