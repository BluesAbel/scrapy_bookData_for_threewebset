# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
import time
class Crawlxiaoshuo(scrapy.Spider):
    name = 'crawldang'
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.03.00.00.00.00.html']

    def parse(self, response):

        #获取小说全部分类的链接
        for i in response.xpath('//*[@id="navigation"]/ul/li[1]/div[2]/div[1]/div/span/a/@href').extract():
            url = 'http://category.dangdang.com' + str(i)
            print(url)
            yield scrapy.Request(url, callback=self.get_url)

        #计算机,考证考研
        urls = ['http://category.dangdang.com/cp01.54.00.00.00.00.html', 'http://category.dangdang.com/cp01.47.00.00.00.00.html']
        for j in urls:
            yield scrapy.Request(j,callback=self.parse)
    def get_url(self,response):

        # 获取下一页
        for i in range(1, 15):
            url = 'http://category.dangdang.com/pg' + str(i) +'-'+ (response.xpath('//*[@id="breadcrumb"]/div/div[3]/a/@href').extract()[0].replace('/',''))
            print(url)
            yield scrapy.Request(url, callback=self.getInfo)

    #解析url内容
    def getInfo(self, response):
        for i in range(1,61):
            try:
                item = DangdangItem()
                item['title'] = response.xpath('//*[@id="component_59"]/li['+str(i)+']/a/@title').extract()[0]
                item['src'] = response.xpath('//*[@id="component_59"]/li['+str(i)+']/a/@href').extract()[0]
                item['price'] = response.xpath('//*[@id="component_59"]/li[' + str(i) + ']/p[3]/span[1]/text()').extract()[0]
                item['num'] = response.xpath('//*[@id="component_59"]/li[' + str(i) + ']//*[@class="search_star_line"]/a/text()').extract()[0].replace('条评论','')
                try:
                    item['press'] = response.xpath('//*[@id="component_59"]/li[' + str(i) + ']/p[5]/span[3]/a/text()').extract()[0]
                except:
                    item['press'] = ''
                item['author'] = response.xpath('//*[@id="component_59"]/li[' + str(i) + ']/p[5]/span[1]/a[1]/text()').extract()[0]
                item['types'] = response.xpath('//*[@id="breadcrumb"]/div/div[3]/a/text()').extract()[0]
                item['big_type'] = '当当'+response.xpath('//*[@id="breadcrumb"]/div/div[2]/a/text()').extract()[0]
                print(item)
                yield item
            except:
                pass
