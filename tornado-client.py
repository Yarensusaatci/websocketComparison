import tornado.ioloop
import tornado.websocket
import time
import logging

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketClient(tornado.websocket.WebSocketClientConnection):
    async def send_message(self, message):
        await self.write_message(message)

async def main():
    uri = "ws://localhost:8888/ws"
    client = await tornado.websocket.websocket_connect(uri)

    try:
        while True:
            message = input("Enter a coin ID to get the price (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            await client.write_message(message)

            response = await client.read_message()
            print(f"Received from server: {response}")
    finally:
        client.close()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
