import csv
import asyncio
import aiohttp
import async_timeout
from scrapy.http import HtmlResponse

results = []


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


def parse(url, body):
    response = HtmlResponse(url=url, body=body)
    for value in response.css('div.col-9.d-inline-block'):
        name = value.xpath('.//a/text()').extract_first().strip()
        update_time = value.xpath('.//@datetime').extract_first()
        results.append((name, update_time))
    return results


async def task(url):
    async with aiohttp.ClientSession() as session:
        http = await fetch(session, url)
        parse(url, http.encode('utf-8'))


def main():
    loop = asyncio.get_event_loop()
    urls = [
        'https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoyMToxNiswODowMM4FkpXb&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNlQxNjoxNzo1MyswODowMM4Bx3_0&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yNFQxNTowMDoxNyswODowMM4BnPdj&tab=repositories'
    ]
    tasks = [task(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('shiyanlou-repos.csv', 'w', newline='') as f_obj:
        writer = csv.writer(f_obj)
        writer.writerows(results)


if __name__ == '__main__':
    main()
