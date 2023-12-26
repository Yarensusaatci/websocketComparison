import tornado.ioloop
import tornado.web
import tornado.websocket
import requests
import time
import concurrent.futures
import logging

COIN_GECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        logger.info("WebSocket connection opened")

    async def on_message(self, message):
        logger.info(f"Received message: {message}")

        try:
            start_time = time.time()

            coin_data = await tornado.ioloop.IOLoop.current().run_in_executor(None, fetch_coin_data, message)
            price_usd = coin_data[message]['usd']

            end_time = time.time()
            latency = end_time - start_time

            self.write_message(f"Price of {message} - ${price_usd} - Latency: {latency} seconds")
            logger.info(f"Response sent for {message}")
        except KeyError:
            self.write_message(f"Could not retrieve price for {message}")
            logger.error(f"Error processing request for {message}")

    def on_close(self):
        logger.info("WebSocket connection closed")

def fetch_coin_data(coin_id):
    response = requests.get(COIN_GECKO_URL.format(coin_id))
    data = response.json()
    return data

def make_app():
    return tornado.web.Application([
        (r"/ws", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    logger.info("WebSocket server listening on port 8888")

    tornado.ioloop.IOLoop.current().start()
