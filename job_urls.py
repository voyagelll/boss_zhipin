import requests 
import time 
import random 
from lxml import etree 
from fake_useragent import UserAgent
from db import *  


class getUrls(object):
	def __init__(self):
		self.redis = RedisClient()
		ua = UserAgent() 
		self.headers = {'User-Agent': ua.random}
		self.cities = {
					'beijing': '101010100', 'shanghai': '101020100', 'guangzhou': '101280000', 'shenzhen': '101280600',
					'hangzhou': '101210100', 'tianjin':'101030000', 'xian': '101110100', 'suzhou': '101190400',
					'wuhan': '101200100', 'xiamen': '101230200', 'changsha': '101250100', 'chengdu': '101270100'}
		self.positions = ['数据分析', '数据挖掘', '爬虫']

	def main(self):
		for city, city_code in self.cities.items():
			for position in self.positions[:]:
				url = 'https://www.zhipin.com/c%s/?query=%s&page=' %(city_code, position)
				for page in range(1, 11):
					print('第 %s 页' % page)
					print(url+str(page))
					rsp = requests.get(url+str(page), headers=self.headers)
					print(rsp)
					text = etree.HTML(rsp.text)
					jobs = text.xpath('//div[@class="job-list"]/ul/li')
					if len(jobs)>0:
						for job in jobs:
							job_url = 'https://www.zhipin.com' + job.xpath('div/div/h3/a/@href')[0]
							# print(job_url)
							self.redis.add_url(job_url)
					else:
						break
					time.sleep(random.randint(5, 8) + random.random()*10)


if __name__ == '__main__':
	g = getUrls()
	g.main()

