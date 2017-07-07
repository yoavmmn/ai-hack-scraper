from flask import Response
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
import html2text
import json
import urllib

class Spider(scrapy.Spider):
  name = "AI-Hack Spider"
  allowed_domain = []
  start_urls = []

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    body = hxs.select("//body/").extract()[0]

    converter = html2text.HTML2Text()
    converter.ignore_links = True
    return converter.handle(body)


def scraper(request, logger):
  request_data = request.get_data()
  logger.debug("received {0}".format(request_data))

  url = "".join(request_data.split("url="))
  url = urllib.unquote(url)

  logger.debug("url {0}".format(url))

  process = CrawlerProcess({
    "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    })

  Spider.allowed_domain.append(url)
  Spider.start_urls.append(url)

  process.crawl(Spider)
  data = process.start()

  logger.debug("scraped motherfucker {0}".format(data))

  return Response(status=200)