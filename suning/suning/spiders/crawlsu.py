# -*- coding: utf-8 -*-
import scrapy
from suning.items import DangdangItem
from copy import deepcopy
import re

class BookSpider(scrapy.Spider):
    name = 'crawlsu'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/1-502320-0.html']

    def parse(self, response):

        # 获取小说全部分类的链接
        b_type = response.xpath('//*[@id="search-path"]/dl/dt/a/text()').extract_first()
        for i in response.xpath('//*[@id="search-opt"]/div/dl[2]/dd/div[1]/div/a')[0:2]:
            url = 'https:' + str(i.xpath('@href').extract()[0])
            types = i.xpath('text()').extract()[0]

            yield scrapy.Request(url, callback=self.get_url,meta={"big_type": b_type,'types':types,'num':1})


        # 计算机,考证考研
        urls = ['https://list.suning.com/1-502308-0.html', 'https://list.suning.com/1-502316-0.html']
        for j in urls:
            yield scrapy.Request(j, callback=self.parse)


    def get_url(self,response):
        # 获取下一页
        for i in range(response.meta['num'], 10):
            try:
                url = 'https://list.suning.com'+(response.xpath('//*[@id="nextPage"]/@href').extract()[0])
                for j in response.xpath('//*[@id="filter-results"]/ul/li/div/div/div/div[1]/div/a/@href').extract():
                    print(j)
                    yield scrapy.Request('https:'+j, callback=self.getInfo,meta={"big_type": response.meta['big_type'],'types':response.meta['types']})
                yield scrapy.Request(url, callback=self.get_url, meta={"big_type": response.meta['big_type'],'types':response.meta['types'],'num':response.meta['num']+1})
            except:
                pass


    def getInfo(self,response):

        item = DangdangItem()

        item['title'] = response.xpath('//*[@id="itemDisplayName"]/text()').extract_first()
        item['src'] = response.url
        item['num'] = response.xpath('//*[@id="productCommTitle"]/a/text()').extract_first().replace('评价（','').replace('）','')

        item['press'] = response.xpath('//*[@id="proinfoMain"]/ul/li[2]/text()').extract_first().replace('\t','').replace('\n','').replace(' ','')

        item['author'] = response.xpath('//*[@id="proinfoMain"]/ul/li[1]/text()').extract_first().replace('\t','').replace('\n','').replace(' ','')
        item['types'] = response.meta['types']
        item['big_type'] = response.meta['big_type']
        item['price'] = str(response.xpath('//*[@id="mainPrice"]/dl[1]/dd/span[1]/text()').extract_first())+str(response.xpath('//*[@id="mainPrice"]/dl[1]/dd/span[1]/span/text()').extract_first())
        if item['price'] == 'None' or item['price'] == 'NoneNone':
            item['price'] = str(response.xpath('//*[@id="mainPrice"]/dl[2]/dd/span[1]/text()').extract_first())+str(response.xpath('//*[@id="mainPrice"]/dl[2]/dd/span[1]/span/text()').extract_first())
        print(item)
        yield item

