import redis

redis_dyjRedis = redis.Redis(host="127.0.0.1", port=6379, db=0)


def upload():
    txt = open("dyjtxt.txt", 'r+')
    for i in txt:
        print i.decode("utf-8")
        redis_dyjRedis.lpush('ItemInBrand', i.decode("utf-8"))
    print "end"
