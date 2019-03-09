import redis 
import re 
import pymongo
import random

# redis数据库地址
REDIS_HOST = '127.0.0.1'
# redis端口
REDIS_PORT = 6379
# redis密码
REDIS_PASSWORD = None 
REDIS_PROXIES = 'proxies'
REDIS_URL = 'url'

# mongo配置
client = pymongo.MongoClient(host='localhost')
dbm = client.project
collection = dbm.boss_zhipin


class RedisClient(object):
	def __init__(self):
		self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

	# 添加url
	def add_url(self, url):
		if not self.db.sismember(REDIS_URL, url):
			return self.db.sadd(REDIS_URL, url)

	# 删除url
	def drop_url(self, url):
		return self.db.srem(REDIS_URL, url)

	# url个数
	def count(self):
		return self.db.scard(REDIS_URL)

	# 获取url
	def get_url(self):
		url = self.db.spop(REDIS_URL)
		if isinstance(url, bytes):
			url = url.decode('utf-8')
		return url

	def get_all_urls(self):
		return self.db.smembers(REDIS_URL)

	def get_proxy(self):
		proxies = self.db.zrangebyscore(REDIS_PROXIES, 10, 10)
		if len(proxies):
			proxy = random.choice(proxies)
			if isinstance(proxy, bytes):
				proxy = proxy.decode('utf-8')
			proxy = {
				'http': 'http://' + proxy,
				'https': 'https://' + proxy
			}
			return proxy


class Mongo(object):
	# def __init__(self):
	def save_data(self, info):
		if collection.insert(info):
			print('save successfully...')
			
		

if __name__ == '__main__':
	redis = RedisClient()
	# print(redis.get_all_urls())

	# urls = redis.get_all_urls()
	# urls = [x.decode('utf-8') for x in urls]
	# print(urls)

	# print(redis.count())

	print(redis.get_proxy())



