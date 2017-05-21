#-*- coding:UTF-8 -*-
import sys

import redis
import tutorial.upload

reload(sys)
sys.setdefaultencoding('utf-8')

class Model:
    JDList = 'https://ai.jd.com/index_new.php?app=ABdata&action=ABData&key=BtestData&callback=getCategoryCallback'

    JD = 'https://www.jd.com'
    JDSearch = "https://search.jd.com/Search?keyword={0}&enc=utf-8&psort=4&click=0"
    TMurl = 'https://list.tmall.com/search_product.htm?q={0}&type=p'
    SNurl = 'http://www.suning.com/'
    YHDurl = 'http://www.yhd.com/'
    YMXurl = 'https://www.amazon.cn/'

    JDDPurl = 'https://item.jd.com/{0}.html'

    JDAllPage = 'https://search.jd.com/Search?keyword={0}&enc=utf-8&psort=4&page={1}&s={2}&click=0'

    JDPLurl = 'https://club.jd.com/comment/skuProductPageComments.action?callback&productId={0}&score=0&sortType=5&page={1}&pageSize=10&isShadowSku=0'
    tutorial.upload.upload()
    redis_dyjRedis = redis.Redis(host='127.0.0.1', port = 6379, db = 0)
    redis_key_phone = "ItemInBrand"
    redis_key_filter = "ItemFilter"
    redis_insert_pl = "dpc_phone_url"
    redis_insert_pl = "dpc_phone_data"

    redis_iplist = "proxy:iplist4"
    redis_iplist2 = "proxy:iplist5"
    redis_iplist3 = "proxy:iplist"
    redis_iplist4 = "proxy:iplist2"
    Phone_name = redis_dyjRedis.keys(redis_key_phone)
    AllNum = 3

    process = 4

    index1,index2,index3,index4 = 0,0,0,0
    lastindex1,lastindex2,lastindex3,lastindex4 = 0,0,0,0

    AllNum = redis_dyjRedis.llen(redis_key_phone)

    numnum = divmod(AllNum, process)

    num = numnum[0]

    yushu = numnum[1]

    i = 1
    index = 0
    lastindex = -1
    while i <= process:
        lastindex += num
        if i == process:
            lastindex += yushu
        if i == 1:
            index1 = index
            lastindex1 = lastindex
        elif i == 2:
            index2 = index
            lastindex2 = lastindex
        elif i == 3:
            index3 = index
            lastindex3 = lastindex
        elif i == 4:
            index4 = index
            lastindex4 = lastindex

        index += num
        i += 1

