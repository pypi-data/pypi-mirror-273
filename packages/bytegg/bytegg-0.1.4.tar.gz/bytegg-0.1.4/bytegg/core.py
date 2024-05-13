import aiohttp
from urllib.parse import quote

async def bypass(*, url, api_key):
    header = {
        "Accept": "/",
        "User-Agent": "Thunder Client (https://www.thunderclient.org/)",
        "Authorization": "Bearer " + api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get("http://paid4.daki.cc:4056/api/bypass?url=" + quote(url), headers=header) as response:
            r = await response.json()
            if "error" in r:
                return r["error"]
            return r["result"]