import json
from unittest.mock import call, patch

import boto3
import responses
from aioresponses import aioresponses
from moto import mock_s3

from main import handler


def load_json_fixture(path):
    json_string = open(path).read()
    json_dict = json.loads(json_string)
    json_string_with_formatting_removed = json.dumps(json_dict)
    return json_string_with_formatting_removed


@aioresponses()
@patch("main.aiobotocore")
@patch("scripts.bitcoin_news.current_time", return_value="2020-01-01T00:00:00.000")
@patch("scripts.bitcoin_price.current_time", return_value="2020-01-01T00:00:00.000")
def test_handler(*mocks):
    mock_aioresponses, _, _, mock_aiobotocore = mocks

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
    Assert S3 put_object called
    """
    mock_session = mock_aiobotocore.get_session.return_value
    mock_context_manager = mock_session.create_client.return_value
    mock_client = mock_context_manager.__aenter__.return_value
    mock_put_object = mock_client.put_object

  
    assert call(
        ACL='public-read',
        Body=load_json_fixture("./tests/fixtures/documents/bitcoin_price.json"),
        Bucket='api.my-bucket.com',
        ContentDisposition='inline',
        ContentType='application/json',
        Key='bitcoin_price.json',
    ) in mock_put_object.mock_calls

    assert call(
        ACL='public-read',
        Body=load_json_fixture("./tests/fixtures/documents/bitcoin_news.json"),
        Bucket='api.my-bucket.com',
        ContentDisposition='inline',
        ContentType='application/json',
        Key='bitcoin_news.json',
    ) in mock_put_object.mock_calls
