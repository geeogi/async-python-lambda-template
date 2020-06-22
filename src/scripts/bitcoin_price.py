import asyncio
import datetime
from dataclasses import asdict

from model.Price import Price
from services.fetch import fetch_json
from services.s3 import write_to_s3


async def bitcoin_price(session, s3_client):
    coingecko, gemini,  blockchain = await asyncio.gather(
        fetch_json(session, "https://api.coingecko.com/api/v3/exchange_rates"),
        fetch_json(session, "https://api.gemini.com/v1/pubticker/btcusd"),
        fetch_json(session, "https://api.blockchain.info/stats")
    )

    prices = [
        Price(
            source="coingecko",
            price=coingecko["rates"]["usd"]["value"]
        ),
        Price(
            source="gemini",
            price=gemini["last"]
        ),
        Price(
            source="blockchain",
            price=blockchain["market_price_usd"]
        )
    ]

    prices_document = {
        'last_updated': datetime.datetime.now().isoformat(),
        'prices': [asdict(price) for price in prices]
    }

    await write_to_s3(prices_document, 'bitcoin_price', client=s3_client)
