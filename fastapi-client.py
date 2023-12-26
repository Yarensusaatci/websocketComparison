import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter a message to send to the server (type 'exit' to close): ")
            await websocket.send(message)

            if message.lower() == 'exit':
                break

            response = await websocket.recv()
            print(f"Received response from server: {response}")

asyncio.get_event_loop().run_until_complete(send_message())
