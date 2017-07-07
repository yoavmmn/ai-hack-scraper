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

  ml_sectors = "ML Machine Learning AI Computer Vision Bots NML Anomaly Detection"

  sectors_list = {
    "fintech": "Payments FinTech Wallet P2P Bitcoin",
    "Machine Learning": ml_sectors,
    "AI": ml_sectors,
    "Transportation": "Drive Cars Autonomous Taxi Bus Train Rail",
    "Cyber": "Cyber Security Intellegence Anomaly Detection Ad Fruad Ransom Virus",
    "Telecom": "Telecom Telekom Phone",
    "IoT": "IoT"
  }

  sectors = []
  keywords = []
  analysis = indicoio.keywords(data, version=2)
  for keyword in analysis:
    keywords.append(keyword)
    for sector in sectors_list:
      if keyword.lower() in sectors_list[sector].lower():
        sectors.append(sectors_list[sector][0])
    

  return str({
    "text": data,
    "keywords": keywords,
    "sectors": sectors
    })