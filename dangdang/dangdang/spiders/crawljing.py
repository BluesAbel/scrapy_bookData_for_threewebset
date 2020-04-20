# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
import time
from copy import deepcopy
import requests
import json
from lxml import etree
class Crawlxiaoshuo(scrapy.Spider):
    name = 'crawljing'
    start_urls = ['https://list.jd.com/list.html?cat=1713,3258']

    def parse(self, response):

        #获取小说全部分类的链接
        for i in response.xpath('//*[@id="J_selectorCategory"]/div/div[2]/div[1]/ul/li/a/@href').extract()[0:2]:
            url = 'https://list.jd.com' + str(i)

            yield scrapy.Request(url, callback=self.get_url)

        #计算机,考证考研
        urls = ['https://list.jd.com/list.html?cat=1713,3258', 'https://list.jd.com/list.html?cat=1713,3290']
        for j in urls:
            yield scrapy.Request(j,callback=self.parse)


    def get_url(self,response):
        # 获取下一页
        for i in range(1, 2):
            url = response.url+'&page='+str(i)+'&sort=sort_rank_asc&trans=1&JL=6_0_0)'
            yield scrapy.Request(url, callback=self.getInfo)

    #解析url内容
    def getInfo(self, response):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        comment_str = ','.join(response.xpath('//*[@id="plist"]/ul/li/div/@data-sku').extract())
        comment_temp_url = "https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds={}"
        comment_url = comment_temp_url.format(comment_str)
        price_temp_url = "https://p.3.cn/prices/mgets?ext=11101000&pin=&type=1&area=1_72_4137_0&skuIds=J_{}"
        price_str = ',J_'.join(response.xpath('//*[@id="plist"]/ul/li/div/@data-sku').extract())
        price_url = price_temp_url.format(price_str)


        response_price = requests.get(price_url, headers=headers)

        price_json = eval(response_price.content.decode("GBK"))
        prices = []
        for i in price_json:
            prices.append(i['p'])



        response_comments = requests.get(comment_url, headers=headers)
        price_json = eval(response_comments.content.decode("GBK"))
        comments = []
        for i in price_json['CommentsCount']:
            comments.append(i['CommentCount'])


        for i in range(1,54):
            try:
                item = DangdangItem()
                li = response.xpath('//ul[@class="gl-warp clearfix"]/li['+str(i)+']')
                item['title'] = li.xpath('.//div[@class="p-name"]/a/em/text()').extract_first().strip()
                item['src'] = 'https:'+response.xpath('//*[@id="plist"]/ul/li['+str(i)+']/div/div[3]/a/@href').extract()[0]
                item['num'] = comments[i-1]
                try:
                    item['press'] = li.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
                except:
                    item['press'] = ''
                item['author'] = li.xpath('.//span[@class="p-bi-name"]/span/a/text()').extract()[0]
                item['types'] = response.xpath('///*[@id="J_crumbsBar"]/div/div/div/div[3]/div/div[1]/span/text()').extract()[0]
                item['big_type'] = '京东'+response.xpath('//*[@id="J_crumbsBar"]/div/div/div/div[2]/div/div[1]/span/text()').extract()[0]
                item['price'] = prices[i-1]
                print(item)
                yield item
            except:
                pass

