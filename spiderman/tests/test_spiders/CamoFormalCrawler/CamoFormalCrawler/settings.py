# -*- coding: utf-8 -*-

# Scrapy settings for CamoFormalCrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CamoFormalCrawler'

SPIDER_MODULES = ['CamoFormalCrawler.spiders']
NEWSPIDER_MODULE = 'CamoFormalCrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CamoFormalCrawler (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    "spiderman.pipelines.SaveItemPipeline": 1000
}

EXTENSIONS = {'scrapy.contrib.feedexport.FeedExporter': None}