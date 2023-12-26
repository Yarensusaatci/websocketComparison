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

# performance.log dosyasına log ekle
file_handler = logging.FileHandler('performance.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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

            logging.info(f"Price of {message} - ${price_usd} - Latency: {latency} seconds")
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

async def run_scalability_test(num_users):
    futures = []

    async def send_request(user_id):
        uri = "ws://localhost:8888/ws"
        async with tornado.websocket.websocket_connect(uri) as client:
            await client.write_message(f"coin-{user_id}")
            response = await client.read_message()
            logger.info(f"User {user_id} - Response: {response}")

    start_time = time.time()

    for user_id in range(num_users):
        tornado.ioloop.IOLoop.current().add_callback(lambda: tornado.ioloop.IOLoop.current().create_task(send_request(user_id)))

    await tornado.gen.sleep(1)  # Bekleme süresi, işlemlerin tamamlanması için yeterli bir süre

    end_time = time.time()
    elapsed_time = end_time - start_time
    throughput = num_users / elapsed_time

    logging.info(f"Scalability Test - {num_users} users processed in {elapsed_time} seconds. Throughput: {throughput} requests/second")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    logger.info("WebSocket server listening on port 8888")

    # Scalability testini başlat
    tornado.ioloop.IOLoop.current().run_sync(lambda: run_scalability_test(10))
    tornado.ioloop.IOLoop.current().start()
