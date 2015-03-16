import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from NewsCrawler.items import HinduItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import glob

class MySpider(scrapy.Spider):

    name = 'TheHindu'
    allowed_domains = ['www.thehindu.com']
    archiveSites = []
    start_urls = []

    def __init__(self, archiveSiteToCrawl = '' , *a, **kw):
        super(MySpider, self).__init__(*a, **kw)
        self.archiveSites = ['%s' % archiveSiteToCrawl]
        
        print "Site to be crawled " + archiveSiteToCrawl
        
        driver = webdriver.Firefox() 
        while(self.archiveSites) :
            self.addNewNewsSites(driver,self.archiveSites)

        driver.close()
        print "No of news sites added " + str(len(self.start_urls))
        # exit()

    def addNewNewsSites(self , driver ,archiveSites) :
        print "Opening site " + archiveSites[len(archiveSites) - 1]
        driver.get(archiveSites.pop())
        time.sleep(10)
        aText = driver.find_elements_by_xpath('//*[@id="left-column"]/div/ul/li/a')
        for sel in aText :
            self.start_urls.append(sel.get_attribute("href"))

    def removeEscapeChars(self, xList) :
        escapeCharSet = ['\n','\r','\t']
        for i in range(len(xList)) :
            for k in escapeCharSet :
                xList[i] = xList[i].replace(k,"")

    def parse(self, response):
        self.log('Crawling %s' % response.url)
        item = HinduItem()
        # textList = response.xpath('//*[@id="left-column"]/div/p/text()').extract()
        textList = response.xpath('//*[@class = "article-text"]/p/text()').extract()
        titleList = response.xpath('//*[@id="left-column"]/h1/text()').extract()
        keyWordList = response.xpath('//*[@id="articleKeywords"]/p/a/text()').extract()
        dateTimeList = response.xpath('//*[@id="left-column"]/div[2]/text()').extract()
        locationList = response.xpath('//*[@id="left-column"]/div[1]/span[2]/span/text()').extract()
        
        item['text'] = ""
        item['title'] = ""
        item['keyWords'] = []
        item['dateTime'] = ""
        item['location'] = ""

        self.removeEscapeChars(textList)
        self.removeEscapeChars(titleList)
        self.removeEscapeChars(keyWordList)
        self.removeEscapeChars(dateTimeList)
        self.removeEscapeChars(locationList)
        
        for x in textList:
            item['text'] = item['text'] + str(x.encode('ascii','ignore'))

        for x in titleList:
            item['title'] = item['title'] + str(x.encode('ascii','ignore'))

        for x in keyWordList:
            item['keyWords'].append(x.encode('ascii','ignore'))

        if dateTimeList:
            item['dateTime'] = dateTimeList[0].encode('ascii', 'ignore')

        if locationList:
            item['location'] = str(locationList[0]).encode('ascii', 'ignore')

        yield item