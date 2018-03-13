# -*- coding: utf-8 -*-
import scrapy
from recruit.items import RecruitItem
from scrapy import Request



class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['zhaopin.com']
    web_frontend = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E6%B7%B1%E5%9C%B3&p=1'
    android_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000& sj=2039&jl=%E6%B7%B1%E5%9C%B3&sm=0&p=1'
    internet_url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=%E6%B7%B1%E5%9C%B3&isadv=0&sg=5f6e91cebcee4fdc81c4e14b97066c07&p=1'
    start_urls = [internet_url]

    # name = 'dd'
    # allowed_domains = ['dangdang.com']
    # start_urls = ['http://search.dangdang.com/?key=python&act=input&page_index=1']

    def __init__(self):
        self.currentPage = 1
        self.totalPage = 90
        self.count = 0;
        process={}
        for i in range(1,91):
            process[i] = {
                'index':0,
                'total':0,
            }
        self.process = process
    def parse(self, response):
        print('currentPage',self.currentPage)
        print('totalPage',self.totalPage)
        item = RecruitItem()
        lis = response.xpath('//td[@class="zwmc"]/div/a/@href')
        # print('len of lif :',lis.extract())
        li_len = len(lis)
        current_page = self.currentPage
        self.process[current_page]['total'] = li_len
        print('li_len',li_len)
        if li_len == 0:
            print('reload')
            # url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E6%B7%B1%E5%9C%B3&p=' + '%d'%self.currentPage
            url = self.internet_url[:len(self.internet_url)-1] + str(current_page)

            print('reload url---',url)
            yield Request(url,callback=self.parse,dont_filter=True)
        else:
            print('else')
            for item in lis:
                # print(item)
                url = item.extract()
                yield Request(url,callback=self.fetch_data,meta={'download_timeout':10},dont_filter=True)
            if self.currentPage < self.totalPage:
                print('next')
                nextPage = current_page + 1
                self.currentPage = nextPage
                # url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&sj=864&jl=%E6%B7%B1%E5%9C%B3&p=' + '%d' % nextPage
                url = self.internet_url[:len(self.internet_url) - 1] + str(nextPage)
                print('next url---', url)
                yield Request(url, meta={'download_timeout': 10}, callback=self.parse, dont_filter=True)

    def fetch_data(self,response):
        current_page = self.currentPage - 1
        print('进度测试', self.process)
        # print('当前页',current_page)
        self.process[current_page]['index'] += 1
        item = RecruitItem()
        item['name'] = response.xpath('//div[@class="top-fixed-box"]/div/div/h1/text()').extract()[0]
        item['pay'] = response.xpath('//div[@class="terminalpage-left"]/ul/li[1]/strong/text()').extract()[0].split('元')[0]
        item['property'] = response.xpath('//div[@class="terminalpage-left"]/ul/li[4]/strong/text()').extract()[0]
        item['experience'] = response.xpath('//div[@class="terminalpage-left"]/ul/li[5]/strong/text()').extract()[0]
        item['min_edu'] = response.xpath('//div[@class="terminalpage-left"]/ul/li[6]/strong/text()').extract()[0]
        item['person'] = response.xpath('//div[@class="terminalpage-left"]/ul/li[7]/strong/text()').extract()[0]
        item['com_scale'] = response.xpath('//div[@class="terminalpage-right"]/div/ul/li[1]/strong/text()').extract()[0].split('人')[0]
        item['com_trade'] = response.xpath('//div[@class="terminalpage-right"]/div/ul/li[3]/strong/a/text()').extract()[0]
        item['com_property'] = response.xpath('//div[@class="terminalpage-right"]/div/ul/li[2]/strong/text()').extract()[0]
        item['page'] = self.currentPage - 1
        self.count +=1;
        print('---------------------- total count%d ---------------'%self.count)
        content = ''
        description = response.xpath('//div[@class="tab-inner-cont"][1]/p/text()')
        for i in description:
            content += i.extract()
        content = content.replace(' ','',9999)
        item['post_description'] = content
        yield item
