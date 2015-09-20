# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CamoformalcrawlerItem(scrapy.Item):
    source_url = scrapy.Field()
    timestamp = scrapy.Field()
    title = scrapy.Field()
    sizes = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
