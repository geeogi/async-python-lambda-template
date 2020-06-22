import asyncio
import datetime
from dataclasses import asdict

from model.News import News
from services.fetch import fetch_text
from services.s3 import write_to_s3


async def bitcoin_news(session, s3_client):
    bbc, wsj, ft, yahoo, coindesk = await asyncio.gather(
        fetch_text(session, "https://www.bbc.co.uk/news"),
        fetch_text(session, "https://www.wsj.com/"),
        fetch_text(session, "https://www.ft.com/"),
        fetch_text(session, "https://uk.finance.yahoo.com/"),
        fetch_text(session, "https://www.coindesk.com/")
    )

    news_sources = [
        News(
            source="bbc",
            is_featured='bitcoin' in bbc
        ),
        News(
            source="wsj",
            is_featured='bitcoin' in wsj
        ),
        News(
            source="ft",
            is_featured='bitcoin' in ft
        ),
        News(
            source="yahoo",
            is_featured='bitcoin' in yahoo
        ),
        News(
            source="coindesk",
            is_featured='bitcoin' in coindesk
        )
    ]

    news_document = {
        'last_updated': datetime.datetime.now().isoformat(),
        'news': [asdict(news_source) for news_source in news_sources]
    }

    await write_to_s3(news_document, 'bitcoin_news', client=s3_client)
