# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiyunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    UserName = scrapy.Field()
    Comment_content = scrapy.Field()
    LikedCount = scrapy.Field()
    Song_name = scrapy.Field()
