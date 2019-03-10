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
from multiprocessing.dummy import Pool 
from db import *

ua = UserAgent() 
redis = RedisClient()
mongo = Mongo()


class parseUrl(object):
	def main(self):
		url_num = redis.count()
		print('当前剩余url：%s' % url_num)
		if url_num>50:
			urls = [url.decode('utf-8') for url in redis.get_all_urls()][:100]
			# 多线程
			pool = Pool(10)
			pool.map(self.coroutine, urls)
			pool.close()
			pool.join()

			# # 协程
			# pool = Pool(50)
			# pool.map(self.coroutine, [url for url in urls])
			# pool.kill()
			# pool.join()
		elif 0<url_num<50:
			urls = [url.decode('utf-8') for url in redis.get_all_urls]
			for url in urls:
				self.coroutine(urls)
		else:
			time.sleep(30)

	def coroutine(self, url):
		headers = {'User-Agent': ua.random}
		proxies = redis.get_proxy()
		try:
			# rsp = requests.get(url, headers=headers)
			rsp = requests.get(url, headers=headers, proxies=proxies)
			text = etree.HTML(rsp.text)
		except:
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
			time.sleep(3)


if __name__ == '__main__':
	p = parseUrl()
	p.main()
