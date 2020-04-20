# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class DangdangPipeline(object):
    def open_spider(self, spider):
        # 定义变量，链接数据库
        self.con = sqlite3.connect('data.db')
        # 定义变量，设置数据库游标
        self.cu = self.con.cursor()

    def process_item(self, item, spider):

        #根据返回的大分类不同,存到不同的表中
        if item['big_type'] == '当当小说':
            insert_sql = 'insert into dangdang_xiaoshuo (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '当当计算机/网络':
            insert_sql = 'insert into dangdang_jisuanji (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '当当考试':
            insert_sql = 'insert into dangdang_kaoshi (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '京东小说':
            insert_sql = 'insert into jingdong_xiaoshuo (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '京东计算机与互联网':
            insert_sql = 'insert into jingdong_jisuanji (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '京东考试':
            insert_sql = 'insert into jingdong_kaoshi (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '苏宁小说':
            insert_sql = 'insert into suning_xiaoshuo (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '苏宁计算机/网络':
            insert_sql = 'insert into suning_jisuanji (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        if item['big_type'] == '苏宁考试':
            insert_sql = 'insert into suning_kaoshi (title, src,price,num,press,author,types) VALUES ( "{}", "{}", "{}", "{}", "{}", "{}","{}")'.format(
                item['title'], item['src'], item['price'], item['num'], item['press'], item['author'], item['types'])
        # 游标执行sql语句
        self.cu.execute(insert_sql)
        # con需要执行提交（插入/更新/删除）操作
        self.con.commit()
        return item

    def spider_close(self, spider):
        self.con.close()
