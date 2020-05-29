import pytest
import requests
from hamcrest import assert_that
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request

from caia.items.items_job_config import ItemsJobConfig
from caia.items.steps.query_source_url import QuerySourceUrl


def test_valid_response_from_server(mock_server):
    with open("tests/resources/items/valid_src_response.json") as file:
        valid_src_response = file.read()

    timestamp = "2020-05-20T00:00:00Z"
    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/items", query={"last_timestamp": timestamp}, operator="deepEquals"),
                             Response(body=valid_src_response)))

    with mock_server(imposter) as server:
        config = {
            'source_url': f"{imposter.url}/items",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/items/items_last_success.txt'
        }
        job_config = ItemsJobConfig(config, 'test')

        query_source_url = QuerySourceUrl(job_config, timestamp)

        step_result = query_source_url.execute()

        assert step_result.was_successful() is True
        assert_that(server, had_request().with_path("/items").and_method("GET"))
        assert valid_src_response == step_result.get_result()


def test_404_response_from_server(mock_server):
    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/items"),
                             Response(status_code=404)))

    with mock_server(imposter) as server:
        config = {
            'source_url': f"{imposter.url}/items",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/items/items_last_success.txt'
        }
        job_config = ItemsJobConfig(config, 'test')

        query_source_url = QuerySourceUrl(job_config, "2020-05-20T00:00:00Z")

        step_result = query_source_url.execute()

        assert step_result.was_successful() is False
        assert_that(server, had_request().with_path("/items").and_method("GET"))
        assert f"Retrieval of '{imposter.url}/items' failed with a status code of 404" in \
               step_result.get_errors()


def test_server_does_not_exist():
    config = {
        'source_url': "http://localhost:12345/URL_DOES_NOT_EXIST",
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt'
    }
    job_config = ItemsJobConfig(config, 'test')

    query_source_url = QuerySourceUrl(job_config, "2020-05-20T00:00:00Z")

    with pytest.raises(requests.exceptions.ConnectionError):
        query_source_url.execute()
