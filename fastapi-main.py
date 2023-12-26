from fastapi import FastAPI
import requests
import time
import logging
import concurrent.futures

app = FastAPI()

logging.basicConfig(filename='performance.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

COIN_GECKO_URL = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd"

def get_coin_gecko_price(coin_id):
    coin_data = requests.get(COIN_GECKO_URL.format(coin_id)).json()
    return coin_data[coin_id]["usd"]

def simulate_user_request(user_id):
    with app.test_client() as c:
        response = c.get(f'/coin/{user_id}')
        logging.info(f"User {user_id} - Response: {response.status_code}")

@app.get("/home")
async def index():
    return {"message": "Greetings!"}

@app.get("/coin/{coin_id}")
async def get_coin_price(coin_id):
    start_time = time.time()

    coin_price = get_coin_gecko_price(coin_id)

    end_time = time.time()
    latency = end_time - start_time

    logging.info(f"Coin: {coin_id} - Price: ${coin_price} - Latency: {latency} seconds")

    return {"message": f"Price of {coin_id} - ${coin_price}", "In Fastapi: latency": f"{latency} seconds"}

@app.get("/scalability-test/{num_users}")
async def scalability_test(num_users: int):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_user_request, user_id) for user_id in range(num_users)]

    concurrent.futures.wait(futures)

    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(f"Scalability Test - {num_users} users completed in {elapsed_time} seconds")

    return {"message": f"In Fastapi: Scalability Test completed for {num_users} users in {elapsed_time} seconds"}

@app.get("/throughput-test/{num_users}")
async def throughput_test(num_users: int):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_user_request, user_id) for user_id in range(num_users)]

    concurrent.futures.wait(futures)

    end_time = time.time()
    elapsed_time = end_time - start_time
    throughput = num_users / elapsed_time  # Throughput hesapla

    logging.info(f"In Fastapi: Throughput Test - {num_users} users processed in {elapsed_time} seconds. Throughput: {throughput} requests/second")

    return {"message": f"Throughput Test completed for {num_users} users in {elapsed_time} seconds", "throughput": throughput}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)