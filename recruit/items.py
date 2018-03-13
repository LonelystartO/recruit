# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() #岗位名称
    pay = scrapy.Field()    # 月工资
    property = scrapy.Field() # 工作性质： 全职
    experience = scrapy.Field() #工作经验
    min_edu = scrapy.Field() #最低学历
    person = scrapy.Field() # 招聘人数
    com_scale = scrapy.Field() # 公司规模
    com_trade = scrapy.Field() # 公司行业
    com_property = scrapy.Field() # 公司性质 ： 合资、民营
    page = scrapy.Field() # 页码
    post_description = scrapy.Field() # 职位描述
