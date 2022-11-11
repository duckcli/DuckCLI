import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        await asyncio.sleep(1)
        return await response.text()


fetch_urls = [
    "https://localhost:9999/ui/inventory",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "https://localhost:9999/ui/inventory/192.168.20.5",
    "http://duckcli.com",
]


async def main():
    urls = fetch_urls
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.extend(fetch(session, url) for url in urls)
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])


if __name__ == "__main__":
    s = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
