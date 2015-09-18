# -*- coding: utf-8 -*-

from datetime import datetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from CamoFormalCrawler.items import CamoformalcrawlerItem
from CamoFormalCrawler.selectors import camoformal_selectors

class CamoformalSpider(CrawlSpider):
    name = "camoformal"
    allowed_domains = ["camoformal.com"]
    start_urls = (
        "http://camoformal.com/wedding/bridal-gowns.html",
    )

    rules = [Rule(LxmlLinkExtractor(allow=[r"/bridal-gowns/\d+"]), callback="parse_item"),
             Rule(LxmlLinkExtractor(allow=[r"bridal-gowns.html\?p=\d+"]))]

    ITEM_CLASS = CamoformalcrawlerItem

    def parse_item(self, response):
        item = CamoformalcrawlerItem()
        item["source_url"] = response.url
        item["timestamp"] = datetime.now().strftime("%d-%m-%y %I:%M:%S %p")
        item["title"] = response.css(camoformal_selectors["title"]).extract()[0]
        item["sizes"] = ", ".join(response.css(camoformal_selectors["sizes"]).extract())
        item["image_urls"] = response.css(camoformal_selectors["image_urls"]).extract()
        return item