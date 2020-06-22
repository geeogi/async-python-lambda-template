async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

async def fetch_text(session, url):
    async with session.get(url) as response:
        return await response.text()
