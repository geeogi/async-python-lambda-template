import json
from unittest.mock import patch

import boto3
import responses
from aioresponses import aioresponses
from moto import mock_s3

from main import handler


@aioresponses()
@patch("main.aiobotocore")
def test_handler(*mocks):
    mock_aioresponses, mock_aiobotocore = mocks
    
    """
    Mock responses for news endpoints 
    """
    mock_aioresponses.get(
        "https://www.bbc.co.uk/news",
        body=open("./tests/fixtures/news/bbc.txt").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://www.wsj.com/",
        body=open("./tests/fixtures/news/wsj.txt").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://www.ft.com/",
        body=open("./tests/fixtures/news/ft.txt").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://uk.finance.yahoo.com/",
        body=open("./tests/fixtures/news/yahoo.txt").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://www.coindesk.com/",
        body=open("./tests/fixtures/news/coindesk.txt").read(),
        status=200
    )

    """
    Mock responses for price endpoints 
    """
    mock_aioresponses.get(
        "https://api.coingecko.com/api/v3/exchange_rates",
        body=open("./tests/fixtures/prices/coingecko.json").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://api.gemini.com/v1/pubticker/btcusd",
        body=open("./tests/fixtures/prices/gemini.json").read(),
        status=200
    ),
    mock_aioresponses.get(
        "https://api.blockchain.info/stats",
        body=open("./tests/fixtures/prices/blockchain.json").read(),
        status=200
    )

    """
    Call handler
    """
    handler(None, None)

    """
    Validate 
    """
    mock_session = mock_aiobotocore.get_session.return_value
    mock_context_manager = mock_session.create_client.return_value
    mock_client = mock_context_manager.__aenter__.return_value
    mock_put_object = mock_client.put_object

    assert len(mock_put_object.mock_calls) == 2
