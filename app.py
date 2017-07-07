import logging
import os

from flask import Flask, request, Response
from scraper import scraper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

@app.route('/echo', methods=['GET'])
def echo():
  return Response(status=200)

@app.route('/scrape', methods=['POST'])
def scrape():
  return scraper(request, logger)

if __name__ == "__main__":
  port = os.getenv('PORT', 5000)

  app.run(host='0.0.0.0', port=port, debug=False)
