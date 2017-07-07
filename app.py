import logging

from flask import Flask, request, Response
from scraper import scraper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

config = {
  "port": 8080
}

app = Flask(__name__)

@app.route('/echo', methods=['GET'])
def echo():
  return Response(status=200)

@app.route('/scrape', methods=['POST'])
def scrape():
  return scraper(request, logger)

app.run(host='0.0.0.0', port=config["port"], debug=True)