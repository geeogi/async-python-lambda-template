from unittest.mock import call, patch

import pytest
from aioresponses import aioresponses
from yarl import URL

from handler import handler
from tests.fixtures.utils import json_fixture, string_fixture


@patch("handler.aiobotocore")
@patch("scripts.bitcoin_news.current_time", return_value="2020-01-01T00:00:00.000")
@patch("scripts.bitcoin_price.current_time", return_value="2020-01-01T00:00:00.000")
def test_handler_fetches_from_http_and_writes_to_s3(_, __, mock_aiobotocore, capsys):
    with aioresponses() as mock_aioresponses:
        """
        Given the news endpoints return fixture data
        """
        mock_aioresponses.get(
            "https://www.bbc.co.uk/news",
            body=string_fixture("news/bbc.txt"),
            status=200
        ),
        mock_aioresponses.get(
            "https://www.wsj.com/",
            body=string_fixture("news/wsj.txt"),
            status=200
        ),
        mock_aioresponses.get(
            "https://www.ft.com/",
            body=string_fixture("news/ft.txt"),
            status=200
        ),
        mock_aioresponses.get(
            "https://uk.finance.yahoo.com/",
            body=string_fixture("news/yahoo.txt"),
            status=200
        ),
        mock_aioresponses.get(
            "https://www.coindesk.com/",
            body=string_fixture("news/coindesk.txt"),
            status=200
        )

        """
        And given the prices endpoints return fixture data
        """
        mock_aioresponses.get(
            "https://api.coingecko.com/api/v3/exchange_rates",
            body=string_fixture("prices/coingecko.json"),
            status=200
        ),
        mock_aioresponses.get(
            "https://api.gemini.com/v1/pubticker/btcusd",
            body=string_fixture("prices/gemini.json"),
            status=200
        ),
        mock_aioresponses.get(
            "https://api.blockchain.info/stats",
            body=string_fixture("prices/blockchain.json"),
            status=200
        )

        """
        When the lambda handler is called
        """
        handler(None, None)

        """
        Then HTTP calls have been made
        """
        expected_urls = ["https://www.bbc.co.uk/news",
                         "https://www.wsj.com/",
                         "https://www.ft.com/",
                         "https://uk.finance.yahoo.com/",
                         "https://www.coindesk.com/",
                         "https://api.coingecko.com/api/v3/exchange_rates",
                         "https://api.gemini.com/v1/pubticker/btcusd",
                         "https://api.blockchain.info/stats"]

        for url in expected_urls:
            assert ('GET', URL(url)) in mock_aioresponses.requests

        """
        And S3 put_object has been called with documents matching fixtures
        """
        mock_session = mock_aiobotocore.get_session.return_value
        mock_context_manager = mock_session.create_client.return_value
        mock_client = mock_context_manager.__aenter__.return_value
        mock_put_object = mock_client.put_object

        assert call(
            Body=json_fixture("documents/bitcoin_price.json"),
            Bucket='python-lambda-s3-bucket',
            ContentDisposition='inline',
            ContentType='application/json',
            Key='bitcoin_price.json',
        ) in mock_put_object.mock_calls

        assert call(
            Body=json_fixture("documents/bitcoin_news.json"),
            Bucket='python-lambda-s3-bucket',
            ContentDisposition='inline',
            ContentType='application/json',
            Key='bitcoin_news.json',
        ) in mock_put_object.mock_calls

        """
        And logs have been written
        """
        log = capsys.readouterr().out
        assert "bitcoin_price written." in log
        assert "bitcoin_news written." in log


@patch("handler.aiobotocore")
@patch("scripts.bitcoin_news.current_time", return_value="2020-01-01T00:00:00.000")
@patch("scripts.bitcoin_price.current_time", return_value="2020-01-01T00:00:00.000")
def test_handler_raises_global_exception_for_bad_request_after_all_scripts_completed(_, __, mock_aiobotocore, capsys):
    with aioresponses() as mock_aioresponses:
        """
        Given some news endpoints return 500
        """
        mock_aioresponses.get("https://www.bbc.co.uk/news", status=500),
        mock_aioresponses.get("https://www.wsj.com/", status=500),
        mock_aioresponses.get("https://www.ft.com/", status=200),
        mock_aioresponses.get("https://uk.finance.yahoo.com/", status=200),
        mock_aioresponses.get("https://www.coindesk.com/", status=200)

        """
        And given a price endpoint returns 400
        """
        mock_aioresponses.get(
            "https://api.coingecko.com/api/v3/exchange_rates", status=400
        ),
        mock_aioresponses.get(
            "https://api.gemini.com/v1/pubticker/btcusd", status=200
        ),
        mock_aioresponses.get(
            "https://api.blockchain.info/stats", status=200
        )

        """
        When the lambda handler is called then an exception is raised
        """
        with pytest.raises(RuntimeError) as err:
            handler(None, None)

            """
            And the stdout explains that both scripts failed
            """
            captured = capsys.readouterr()
            assert "bitcoin_price failed" in captured.out
            assert "bitcoin_news failed" in captured.out

            """
            And the stderr details both HTTP exceptions, one from each script
            """
            assert "ClientResponseError: 400, message='Bad Request'" in captured.err
            assert "ClientResponseError: 500, message='Internal Server Error'" in captured.err
