# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest, Request
from SearchDisconnectCrawler.items import SearchdisconnectcrawlerItem


class SearchdisconnectSpider(CrawlSpider):
  name = "searchdisconnect"
  allowed_domains = ["https://search.disconnect.me/"]
  start_urls = (
      'https://search.disconnect.me/',
  )

  rules = [Rule(LxmlLinkExtractor(restrict_xpaths=["//div[@class='pagination']"]),
                callback="parse_links")]

  ITEM_CLASS = SearchdisconnectcrawlerItem

  def __init__(self, keyword="porn", *args, **kwargs):
    super(SearchdisconnectSpider, self).__init__(*args, **kwargs)
    self._query = keyword

  def parse_start_url(self, response):
    return FormRequest.from_response(response, formdata={"query":self._query}, callback=self.parse_links)

  def parse_links(self, response):
    item = SearchdisconnectcrawlerItem()
    item["keyword"] = self._query
    urls = response.css("a.title::attr(href)").extract()
    for url in urls:
      item["url"] = url
      yield item
    pagination_links = response.css("div.pagination a::attr(href)").extract()
    for link in pagination_links:
      yield Request(self.start_urls[0] + "searchTerms/" + link[2:], callback=self.parse_links)
