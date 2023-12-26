import socketio
import requests
import time
import logging

# Logger'ı yapılandır
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# performance.log dosyasına log ekle
file_handler = logging.FileHandler('performance.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('response')
def handle_response(data):
    print(f"Server response: {data['data']}")

if __name__ == '__main__':
    # Socket.IO server adresini belirtin
    server_url = 'http://localhost:5000'

    # Socket.IO server'la bağlantı kurun
    sio.connect(server_url)

    try:
        while True:
            start_time = time.time()

            message = input("Enter a coin ID to get the price (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            # Server'a coin ID gönderin
            sio.emit('message', message)

            end_time = time.time()
            latency = end_time - start_time
            logger.info(f"Latency for {message}: {latency} seconds")
    finally:
        # Bağlantıyı kapatın
        sio.disconnect()

