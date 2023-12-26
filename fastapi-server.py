import asyncio
import websockets

async def handle_client(websocket, path):
    while True:
        try:
            message = await websocket.recv()
            print(f"Received message from client: {message}")

            # Sunucudan istemciye cevap gönderme
            response = f"Server received: {message}"
            await websocket.send(response)
        except websockets.exceptions.ConnectionClosedOK:
            print("Client disconnected")
            break

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
