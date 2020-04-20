# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
from copy import deepcopy
import re


class BookSpider(scrapy.Spider):
    name = 'crawlsu'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/1-502320-0.html']

    def parse(self, response):

        # 获取小说全部分类的链接
        for i in response.xpath('//*[@id="search-opt"]/div/dl[2]/dd/div[1]/div/a'):
            url = 'https:' + str(i.xpath('@href').extract()[0])
            types = response.xpath(i.xpath('text()').extract()[0])
            yield scrapy.Request(url, callback=self.get_url,meta={"big_type": '苏宁小说','types':types})

        # # 计算机,考证考研
        # urls = ['https://list.jd.com/list.html?cat=1713,3258', 'https://list.jd.com/list.html?cat=1713,3290']
        # for j in urls:
        #     yield scrapy.Request(j, callback=self.parse)


    def get_url(self,response):

        # 获取下一页
        for i in range(1, 15):
            url = 'http://category.dangdang.com/pg' + str(i) +'-'+ (response.xpath('//*[@id="breadcrumb"]/div/div[3]/a/@href').extract()[0].replace('/',''))
            print(url)
            yield scrapy.Request(url, callback=self.getInfo)













    # 处理每个分类下的图书
    def process_cate_url(self, response):

        item = response.meta["item"]
        product_lists = response.xpath("//div[@id='filter-results']//li[contains(@class, 'product')]")

        for product in product_lists:
            item["book_img_url"] = "https:"+product.xpath(".//img/@src2").extract_first()
            item["book_name"] = product.xpath(".//img/@alt").extract_first()
            item["book_detail_url"] = "https:"+product.xpath(".//a[@class='sellPoint']/@href").extract_first()
            item["book_comments_num"] = product.xpath(".//p[@class='com-cnt']/a[1]/text()").extract_first()

            item["price_url_param1"] = product.xpath("./@class").extract_first()
            item["price_url_param1"] = re.sub("\s+","-",item["price_url_param1"]).split("-")

            item['cp'] = None
            item['ci'] = None
            item['currentPage'] = None
            item['pageNumbers'] = None




            # 处理每一本图书详情页
            yield scrapy.Request(
                item["book_detail_url"],
                callback=self.process_book_detail,
                meta={"item":deepcopy(item)}
            )


        item['ci'] = response.request.url.split('-')[-2]
        item['currentPage'] = int(re.findall('param.currentPage = "(.*?)";', response.body.decode())[0])
        item['pageNumbers'] = int(re.findall('param.pageNumbers = "(.*?)";',response.body.decode())[0])


        item['cp'] = item['currentPage']
        # 上面的连接只能获得前30本书，一共有60本书，后半段在另一个链接里
        next_part_url = "https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=010&paging=1&sub=0".format(item['ci'],item['cp'])

        # print(next_part_url)

        yield scrapy.Request(
            next_part_url,
            callback=self.process_next_product,
            meta={"item":deepcopy(item)}

        )




    def process_next_product(self, response):

        item = response.meta["item"]
        product_lists = response.xpath("//div[@id='filter-results']//li[contains(@class, 'product')]")

        for product in product_lists:
            item["book_img_url"] = "https:" + product.xpath(".//img/@src2").extract_first()
            item["book_name"] = product.xpath(".//img/@alt").extract_first()
            item["book_detail_url"] = "https:" + product.xpath(".//a[@class='sellPoint']/@href").extract_first()
            item["book_comments_num"] = product.xpath(".//p[@class='com-cnt']/a[1]/text()").extract_first()

            item["price_url_param1"] = product.xpath("./@class").extract_first()
            item["price_url_param1"] = re.sub("\s+", "-", item["price_url_param1"]).split("-")

            # 处理每一本图书详情页
            yield scrapy.Request(
                item["book_detail_url"],
                callback=self.process_book_detail,
                meta={"item": deepcopy(item)}
            )

        # # 翻页
        if item['currentPage'] < item['pageNumbers']:

            item['cp'] =item['currentPage'] + 1
            next_page_url = "https://list.suning.com/emall/showProductList.do?ci={}&pg=03&cp={}&il=0&iy=0&adNumber=0&n=1&ch=4&prune=0&sesab=ACBAAB&id=IDENTIFYING&cc=010".format(item['ci'],item['cp'])

            yield scrapy.Request(
                next_page_url,
                callback=self.process_next_product,
                meta={"item": deepcopy(item)}
            )



    def process_book_detail(self, response):

        item = response.meta["item"]

        item["book_author"] = response.xpath("//ul[contains(@class, 'bk-publish')]/li[1]/text()").extract_first()
        item["book_author"] = re.sub("\s","",item["book_author"]) if item["book_author"] else None

        item["book_publisher"] = response.xpath("//ul[contains(@class, 'bk-publish')]/li[2]/text()").extract_first()
        item["book_publisher"] = re.sub("\s","",item["book_publisher"]) if item["book_publisher"] else None

        item["book_publish_date"] = response.xpath("//ul[contains(@class, 'bk-publish')]/li[3]/span[2]/text()").extract_first()

        item["price_url_param2"] = re.findall('"weight":"(.*?)",', response.body.decode())[0]


        # print(item["price_url_param1"][2])
        # print(item["price_url_param2"])

        param1 = item["price_url_param1"][2]
        param2 = item["price_url_param1"][3]
        param3 = item["price_url_param2"]
        item['book_price_url'] = "https://pas.suning.com/nspcsale_0_000000000{}_000000000{}_{}_10_010_0100101_502282_1000000_9017_10106_Z001___R9011205_{}___.html".format(param1,param1,param2,param3)

        # print(price_url)

        # 获取价格
        yield scrapy.Request(
            item['book_price_url'],
            callback=self.get_price,
            meta={"item":deepcopy(item)}
        )


    def get_price(self, response):

        item = response.meta["item"]
        book_price = re.findall('"netPrice":"(.*?)",', response.body.decode())
        item["book_price"] = book_price[0] if book_price else None

        yield item


