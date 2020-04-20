# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #商品名称
    title = scrapy.Field()
    #链接
    src = scrapy.Field()
    #价格
    price = scrapy.Field()
    #评论数
    num = scrapy.Field()
    #出版社
    press = scrapy.Field()
    #作者
    author = scrapy.Field()
    #小分类
    types = scrapy.Field()
    #大分类
    big_type = scrapy.Field()
    pass
