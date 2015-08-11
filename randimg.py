import random
import string
import asyncio
import aiohttp

@asyncio.coroutine
def randomness():
    url_pattern = "http://i.imgur.com/{}{}{}{}{}.jpg"
    url_symbols = string.digits + string.ascii_letters
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.10 Safari/537.36'}
    imgur_url = url_pattern.format(*(random.choice(url_symbols) for _ in range(5)))
    r = yield from aiohttp.request('head', imgur_url)
    while r.status != 200 or "removed" in r.url:
        imgur_url = url_pattern.format(*(random.choice(url_symbols) for _ in range(5)))
        r = yield from aiohttp.request('head', imgur_url)
    return imgur_url