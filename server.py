import logging

from scraper import scraper
from flask import Flask, request, Response

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

config = {
  "port": 80
}

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
  return scraper(request, logger)

app.run(host='0.0.0.0', port=config["port"], debug=True)