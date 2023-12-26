import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
def message(sid, data):
    print(f"Message from {sid}: {data}")
    # Burada gelen mesajı işleyebilir ve istemciye yanıt gönderebilirsiniz
    sio.emit('response', {'data': 'Server received your message'}, room=sid)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    # Flask uygulamasını oluşturun
    flask_app = Flask(__name__)

    # Socket.IO uygulamasını Flask uygulamasına bağlayın
    flask_app.wsgi_app = socketio.WSGIApp(sio, flask_app.wsgi_app)

    # Flask uygulamasını çalıştırın
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), flask_app)
