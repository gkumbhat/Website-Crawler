import csv
import sys
import time
import threading
from scrapy.spiders import Spider
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

	
class crawlData(Spider):
	
	def crawl_data(self, link):	
		
		self.browser.get(link)
		#To sort the pages by end date
		button = self.browser.find_elements_by_xpath("//*[@id='project_table']/thead/tr/th")
		button[3].click()
		#To run while there is next page present:
		oldButtonLink = ""
		while True:
			#browser.get('http://www.freelancer.com/jobs/1') 
			#base =  browser.find_elements_by_xpath('//tr[@class="odd project-details"]')
			data=[]
			time.sleep(1)
			base =  self.browser.find_elements_by_xpath('//tr[contains(@class,"odd project-details") or contains(@class,"even project-details")]')
			for x in range(0,len(base)):
				project_id=base[x].get_attribute("project_id")
				link=base[x].find_element_by_xpath('.//td[@class=" title-col"]/a')
				title=base[x].find_element_by_xpath('.//td[@class=" title-col"]/a')
				started=base[x].find_element_by_xpath('.//td[@class=" started-col sorting_1"]')
				tempData={};
				tempData['title'] = title.text.encode("utf-8")
				tempData['link'] = link.get_attribute("href").encode("utf-8")
				tempData['started'] = started.get_attribute('innerHTML').replace("<small>Ended</small>","").encode("utf-8")
				tempData['projectid'] = project_id
				data.append(tempData)
			print len(data)
			keys = []
			if len(data) != 0:
				keys = data[0].keys()
			else:
				print "Length is zero"

			for i in range(0, len(data)):
				if data[i]['started'].__contains__('Today'):
					data[i]['started'] = time.strftime("%b %d, %Y")
			print data[0]['started']
			#print data[1]['started']
			with open('test.csv', 'a') as f:
				wtr = csv.DictWriter(f, keys)
				#wtr.writeheader()
				try:
					wtr.writerows(data)
				except UnicodeEncodeError:
					wtr.writerows(data)
					pass
			try:
				nextButton = self.browser.find_element_by_xpath("//*[@class='next paginate_button table_paginate']/a")
				if (nextButton.get_attribute("href") == oldButtonLink):
					print "-----------------Last Page Reached--------------------"
					break;
				oldButtonLink = nextButton.get_attribute("href")
				nextButton.click()
				

			except:
				print sys.exc_info()[0]
				print sys.exc_info()[1]

	def __init__(self, *args, **kwargs):
		self.browser=webdriver.Firefox()
		#self.browser = webdriver.PhantomJS()
		#self.browser.set_window_size(1024, 768)
		
	def __del__(self):
		self.browser.quit()

	def spider_closed(self, spider):
		self.browser.quit()

if __name__ == '__main__':
	i=1
	test = crawlData()

	try:
		test.crawl_data("http://www.freelancer.com/jobs/" + str(i))
			
	except:
		print sys.exc_info()[0]
		print sys.exc_info()[1]
		
	