import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def main():
    urls = [
        "https://localhost:9999/ui/inventory",
        "https://localhost:9999/ui/inventory/192.168.20.5",
    ]
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.extend(fetch(session, url) for url in urls)
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
