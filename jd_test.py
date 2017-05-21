#-*- coding:UTF-8 -*-

import sys
import threading
import time

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


if __name__== '__main__':
    AllSearch_JD()