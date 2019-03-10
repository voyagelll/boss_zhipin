from job_urls import * 
from parse_urls import * 
from db import * 
from multiprocessing import Process
import time 


class Scheduler(object):
	def __init__(self):
		self.redis = RedisClient()
		
	def schedule_get(self):
		g = getUrls()
		g.main()
		
	def schedule_parse(self):
		p = parseUrl()
		while True:
			p.main()

	def run(self):
		test_jobs = Process(target=self.schedule_get)
		test_jobs.start()

		test_parse_job = Process(target=self.schedule_parse)
		test_parse_job.start() 


if __name__ == '__main__':
	s = Scheduler()
	s.run()