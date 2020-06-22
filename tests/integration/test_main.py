from unittest.mock import patch

import boto3
import responses
from moto import mock_s3
import json

from main import handler


@responses.activate
@patch("main.aiobotocore")
def test_handler(mock_aiobotocore):
    """
    Mock responses for news endpoints 
    """
    responses.add(
        method=responses.GET,
        url="https://www.bbc.co.uk/news",
        body=open("./tests/fixtures/news/bbc.txt").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://www.wsj.com/",
        body=open("./tests/fixtures/news/wsj.txt").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://www.ft.com/",
        body=open("./tests/fixtures/news/ft.txt").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://uk.finance.yahoo.com/",
        body=open("./tests/fixtures/news/yahoo.txt").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://www.coindesk.com/",
        body=open("./tests/fixtures/news/coindesk.txt").read(),
        status=200
    )

    """
    Mock responses for price endpoints 
    """
    responses.add(
        method=responses.GET,
        url="https://api.coingecko.com/api/v3/exchange_rates",
        body=open("./tests/fixtures/prices/coingecko.json").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://api.gemini.com/v1/pubticker/btcusd",
        body=open("./tests/fixtures/prices/gemini.json").read(),
        status=200
    ),
    responses.add(
        method=responses.GET,
        url="https://api.blockchain.info/stats",
        body=open("./tests/fixtures/prices/blockchain.json").read(),
        status=200
    )

    """
    Call handler
    """
    handler(None, None)

    mock_session = mock_aiobotocore.get_session.return_value
    mock_context_manager = mock_session.create_client.return_value
    mock_client = mock_context_manager.__aenter__.return_value
    mock_put_object = mock_client.put_object
