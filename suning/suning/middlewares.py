# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.chrome.options import Options


class SpiderMiddleware(object):

    def __init__(self):
        option = Options()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=option)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        self.driver.execute_script("scroll(0, 1000);")
        time.sleep(1)
        rendered_body = self.driver.page_source
        return HtmlResponse(request.url, body=rendered_body, encoding="utf-8")

    def spider_closed(self, spider, reason):
        print('驱动关闭')
        self.driver.close()
