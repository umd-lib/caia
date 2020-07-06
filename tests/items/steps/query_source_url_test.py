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

    last_timestamp = "20200601"
    current_timestamp = "20200603"

    # Set up mock server with required behavior
    imposter = Imposter(
                   Stub(
                       Predicate(path="/items",
                                 query={"starttime": last_timestamp, "endtime": current_timestamp},
                                 operator="deepEquals"),
                       Response(body=valid_src_response)
                   )
                )

    with mock_server(imposter) as server:
        config = {
            'source_url': f"{imposter.url}/items",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/items/items_last_success.txt'
        }
        job_config = ItemsJobConfig(config, 'test')

        query_source_url = QuerySourceUrl(job_config, last_timestamp, current_timestamp, None)

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

        last_timestamp = "20200601"
        current_timestamp = "20200603"

        query_source_url = QuerySourceUrl(job_config, last_timestamp, current_timestamp, None)

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

    last_timestamp = "20200601"
    current_timestamp = "20200603"

    query_source_url = QuerySourceUrl(job_config, last_timestamp, current_timestamp, None)

    with pytest.raises(requests.exceptions.ConnectionError):
        query_source_url.execute()
