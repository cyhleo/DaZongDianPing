# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DazongdianpingItem(scrapy.Item):
    # define the fields for your item here like:
    #店名
    shop = scrapy.Field()
    #点评人数
    comment_num = scrapy.Field()
    #人均
    per_capita = scrapy.Field()
    #菜系
    type_food = scrapy.Field()
    #商区
    business_zone = scrapy.Field()
    #位置
    location = scrapy.Field()
    #口味分数
    taste = scrapy.Field()
    #环境分数
    env = scrapy.Field()
    #服务分数
    serve = scrapy.Field()
    _id = scrapy.Field()

