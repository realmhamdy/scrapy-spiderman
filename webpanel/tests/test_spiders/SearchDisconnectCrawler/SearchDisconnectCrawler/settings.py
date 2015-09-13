# -*- coding: utf-8 -*-

# Scrapy settings for SearchDisconnectCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'SearchDisconnectCrawler'

SPIDER_MODULES = ['SearchDisconnectCrawler.spiders']
NEWSPIDER_MODULE = 'SearchDisconnectCrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SearchDisconnectCrawler (+http://www.yourdomain.com)'

DOWNLOAD_DELAY = 5
FEED_FORMAT = "csv"
FEED_URI = r"/output/results.csv"
SPIDER_MIDDLEWARES = {'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None}