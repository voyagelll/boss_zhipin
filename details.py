import requests 
import time 
import random 
import re 
from lxml import etree 
from fake_useragent import UserAgent 
# import gevent 
# from gevent import monkey 
# gevent.monkey.patch_all()
# from gevent import Timeout 
# from gevent.pool import Pool
from db import *

ua = UserAgent() 
redis = RedisClient()
mongo = Mongo()


def coroutine(url):
	if redis.count():
		headers = {'User-Agent': ua.random}
		proxies = redis.get_proxy()
		# rsp = requests.get(url, headers=headers, proxies=proxies)
		# print(rsp)
		try:
			rsp = requests.get(url, headers=headers)
			# rsp = requests.get(url, headers=headers, proxies=proxies)
			text = etree.HTML(rsp.text)
		except:
			# redis.add_url(url)
			# print(e)
			pass
		else:
			print(redis.count(), url)
			redis.drop_url(url)
			info = {}
			# 岗位
			try:
				info['job'] = text.xpath('//div[@class="company-info"]/div/h1/text()')[0]
			except:
				info['job'] = ''
			# 薪资
			try:
				salary = text.xpath('//div[@class="company-info"]/div/span/text()')[0]
				info['salary'] = re.search('\d+-\d+', salary)[0]
			except:
				info['salary'] = ''
			# 地点
			try:
				info['location'] = text.xpath('//div[@class="info-primary"]/p/text()')[0]
			except:
				info['location'] = ''
			# 工作经验
			try:
				info['experience'] = text.xpath('//div[@class="info-primary"]/p/text()')[1]
			except:
				info['experience'] = ''
			# 学历要求
			try:
				info['degree'] = text.xpath('//div[@class="info-primary"]/p/text()')[2]
			except:
				info['degree'] = ''
			# 福利
			try:
				bonus = text.xpath('//div[@class="info-primary"]/div[@class="tag-container"]/div/div/span/text()')
				info['bonus'] = '\t'.join(bonus)
			except:
				info['bonus'] = ''
			# 工作描述
			desc = text.xpath('//div[@class="detail-content"]/div[1]/div[1]/text()')
			desc = ''.join(desc).replace('\n', '').replace(',', '\t').replace('，', '\t').strip()
			requirements = ''
			if '要求' in desc:
				descs = desc.split('要求')
				info['job_desc'] = descs[0]
				info['requirements'] = descs[1]
			elif '任职资格' in desc:
				descs = desc.split('任职资格')
				info['job_desc'] = descs[0]
				info['requirements'] = descs[1]
			else:
				info['job_desc'] = ''.join(desc).replace('\n', '').replace(',', '\t').replace('，', '\t').strip()
			# 公司名称
			try:
				info['company'] = text.xpath('//div[@class="sider-company"]/div/a/@title')[0]
			except:
				info['company'] = ''
			# 员工人数
			try:
				staff_num = text.xpath('//div[@class="sider-company"]/p[3]/text()')[0]
				info['staff_num'] = re.search('\d+-\d+', staff_num)[0]
			except:
				info['staff_num'] = 0
			# 发布时间
			try:
				info['release_time'] = text.xpath('//div[@class="sider-company"]/p[@class="gray"]/text()')[0][4:]
				# info['release_time'] = re.search('\d+-\d+', staff_num)[0]
			except:
				info['release_time'] = 0
			# print(info)
			mongo.save_data(info)


if __name__ == '__main__':
	# coroutine(redis.get_url())

	# urls = redis.get_all_urls()
	# urls = [x.decode('utf-8') for x in urls]
	# pool = Pool()
	# pool.map(coroutine, [url for url in urls])
	# pool.kill()
	# pool.join()

	coroutine('https://www.zhipin.com/job_detail/2ccbe10e376ea6451HRy3dy-FlE~.html')