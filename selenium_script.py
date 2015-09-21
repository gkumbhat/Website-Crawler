import csv
import sys
import time
from scrapy.spiders import Spider
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
	
class crawlData(Spider):
	
	def crawl_data(self, link):	
		#browser.get('http://www.freelancer.com/jobs/1') 
		self.browser.get(link)
		#base =  browser.find_elements_by_xpath('//tr[@class="odd project-details"]')
		data=[]
		base =  self.browser.find_elements_by_xpath('//tr[contains(@class,"odd project-details") or contains(@class,"even project-details")]')
		for x in range(0,len(base)):
			project_id=base[x].get_attribute("project_id")
			link=base[x].find_element_by_xpath('.//td[@class=" title-col"]/a')
			title=base[x].find_element_by_xpath('.//td[@class=" title-col"]/a')
			started=base[x].find_element_by_xpath('.//td[@class=" started-col sorting_1"]')
			tempData={};
			tempData['title'] = title.text.encode("utf-8")
			tempData['link'] = link.get_attribute("href").encode("utf-8")
			tempData['started'] = started.text.encode("utf-8")
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
		print data[1]['started']
		with open('test.csv', 'a') as f:
			wtr = csv.DictWriter(f, keys)
			#wtr.writeheader()
			try:
				wtr.writerows(data)
			except UnicodeEncodeError:
				wtr.writerows(data)
				pass
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	def __init__(self, *args, **kwargs):
		#self.browser=webdriver.Firefox()
		self.browser = webdriver.PhantomJS()
		self.browser.set_window_size(1024, 768)
		#super(MySpider, self).__init__(*args, **kwargs)
        #SignalManager(dispatcher.Any).connect(self.spider_closed, signal=signals.spider_closed)

	def __del__(self):
		self.browser.quit()

	def spider_closed(self, spider):
		self.browser.quit()

if __name__ == '__main__':
	i=3005
	test = crawlData()
	while True:
		try:
			test.crawl_data("http://www.freelancer.com/jobs/" + str(i))
			i=i+1
			print i
		except:
			#print sys.exc_info()[0]
			#print sys.exc_info()[1]
			break;