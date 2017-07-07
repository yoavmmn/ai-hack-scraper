from flask import Response
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import BaseSpider
import scrapy
import html2text
import json
import urllib
import requests
import lxml.html

class Spider(scrapy.Spider):
  name = "AI-Hack Spider"
  allowed_domain = []
  start_urls = []

  def parse(self, response):
    results = []

    results.append(self.getHtml(response))

    return results

  def getHtml(self, response):
    hxs = scrapy.Selector(response)

    return {
      "text": ''.join(hxs.xpath("//body//text()").extract()).strip()
    }


def scraper(request, logger):
  request_data = request.get_data()
  logger.debug("received {0}".format(request_data))

  url = "".join(request_data.split("url="))
  url = urllib.unquote(url)

  logger.debug("url {0}".format(url))

  # process = CrawlerProcess({
  #   "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
  #   })

  # Spider.start_urls = [url]
  # Spider.allowed_domain = [url]

  # logger.debug("allowed_domain {0} start_urls {1}".format(Spider.allowed_domain, Spider.start_urls))

  # process.crawl(Spider)
  # data = process.start()

  # logger.debug("scraped motherfucker {0}".format(data))
  # 
  r = requests.get(url)
  tree = lxml.html.fromstring(r.text)
  data = tree.xpath("//body")[0].text_content()

  return {"text": data}