from flask import Response
import json
import urllib
import requests
import lxml.html
import indicoio
import os

indicoio.config.api_key = os.getenv('indicoio_key')

def scraper(request, logger):
  request_data = request.get_data()
  logger.debug("received {0}".format(request_data))

  url = "".join(request_data.split("url="))
  url = urllib.unquote(url)

  logger.debug("url {0}".format(url))

  r = requests.get(url)
  tree = lxml.html.fromstring(r.text)
  data = tree.xpath("//body")[0].text_content()

  data = ''.join(data.split('\n'))

  keyowrds = []
  analysis = indicoio.keywords(data, version=2)
  for keyword in analysis:
    keywords.append(keyword)

  return str({
    "text": data,
    "keywords": keywords})