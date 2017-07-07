from flask import Response
import json
import urllib
import requests
import lxml.html
import indicoio
import os

indicoio.config.api_key = os.getenv('indicoio_key')

def scraper(request, logger):
  request_data = request.args.get('url')
  logger.debug("received {0}".format(request_data))

  url = request.args.get('url')
  url = urllib.unquote(url)
  headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
  }

  logger.debug("url {0}".format(url))

  r = requests.get(url, headers=headers)
  tree = lxml.html.fromstring(r.text)
  data = tree.xpath("//body")[0].text_content()

  data = ''.join(data.split('\n'))

  ml_sectors = "ML Machine Learning AI Computer Vision Bots NML Anomaly Detection artificial intelligence"

  sectors_list = {
    "iot": "IoT",
    "ai": ml_sectors,
    "machine learning": ml_sectors,
    "telecom": "Telecom Telekom Phone",
    "fintech": "Payments FinTech Wallet P2P Bitcoin",
    "transportation": "Drive Cars Autonomous Taxi Bus Train Rail",
    "cyber": "Cyber Security intelligence Anomaly Detection Ad Fruad Ransom Virus Defense Attack",
  }

  logger.debug(u"data: {0}".format(data))

  sectors = []
  keywords = []
  analysis = indicoio.keywords(data, version=2)

  for keyword in analysis:
    keywords.append(keyword)
    for sector in sectors_list:
      if keyword.lower() in sectors_list[sector].lower():
        if not sector in sectors:
          sectors.append(sector)
    

  return str({
    "text": data,
    "keywords": keywords,
    "sectors": sectors
    })