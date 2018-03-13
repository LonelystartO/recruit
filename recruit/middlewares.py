# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
# from .settings import IPPOOL

class RandomProxyMiddleware(object):
    '''动态设置ip代理'''
    def __init__(self):
        self.ip_pool = [
            "1.180.235.164:3128",
            "14.29.47.90:3128",
            "219.135.164.245:3128"
        ]
    def process_request(self, request, spider):
        print('pool ------' + random.choice(self.ip_pool))
        get_ip = random.choice(self.ip_pool)  # 这里的函数是传值ip的
        request.meta["proxy"] = get_ip
    def process_exception(self,request, exception, spider):
        # print('change pool ------' + random.choice(self.ip_pool))
        # print('exception' + exception)
        get_ip = random.choice(self.ip_pool)  # 这里的函数是传值ip的
        request.meta["proxy"] = get_ip
        return request

class RecruitSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self,crawler):
        super(RecruitSpiderMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')  # 从setting文件中读取RANDOM_UA_TYPE值
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)
        user_agent_random = get_ua()
        # print('current ua is : ' + user_agent_random)
        request.headers.setdefault('User-Agent', user_agent_random)  # 这样就是实现了User-Agent的随即变换

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
