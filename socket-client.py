import socketio

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
            message = input("Enter a message to send to the server (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break

            # Server'a mesaj gönderin
            sio.emit('message', message)
    finally:
        # Bağlantıyı kapatın
        sio.disconnect()
