'''
    此文件为redis数据库操作模块，将数据库得操作封装为一个个函数
    用来将获取得cookies保存以便于调用
    2021年3月2日
    作者：焦康阳  https://jiaokangyang.com
'''
import redis
import random

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

class RedisClient(object):
    def __init__(self,name,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        # 链接数据库
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)
        # 这块用来标记存储得数据是什么，例如账号，cookies我们进行区分
        self.name = name

    # 写入数据,这里得username是京东的账号，value为密码或者cookies
    def set(self,username,value):
        return self.db.hset(self.name,username,value)

    # 根据账号获取value
    def get(self,username):
        return self.db.hget(self.name,username)

    # 根据账号删除键值对
    def delete(self,username):
        return self.db.hdel(self.name,username)

    # 获取个数
    def count(self):
        return self.db.hlen(self.name)

    # 随机获取value，我们这里主要后期用来获取cookies
    def random(self):
        return random.choice(self.db.hvals(self.name))

    # 获取所有的账号
    def usernames(self):
        return self.db.hkeys(self.name)

    # 获取所有键值对
    def all(self):
        return self.db.hgetall(self.name)

    # 随机获取一组字段和值
    def random_getall(self):
        # 随机获取一个账号
        username = random.choice(self.usernames())
        # 获取该账号的值
        cookie = self.get(username)
        return username,cookie

    # 删除key
    def clear(self):
        return self.db.delete(self.name)