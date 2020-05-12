from hamcrest import assert_that
from mbtest.matchers import had_request
from mbtest.imposters import Imposter, Predicate, Response, Stub
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.steps.query_source_url import QuerySourceUrl
import pytest
import requests


def test_valid_response_from_server(mock_server):
    with open("tests/resources/circrequests/valid_src_response.json") as file:
        valid_src_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/holds"),
                             Response(body=valid_src_response)))

    with mock_server(imposter) as server:
        config = {
            'source_url': f"{imposter.url}/holds",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt'
        }
        job_config = CircrequestsJobConfig(config, 'test')

        query_source_url = QuerySourceUrl(job_config)

        step_result = query_source_url.execute()

        assert step_result.was_successful() is True
        assert_that(server, had_request().with_path("/holds").and_method("GET"))


def test_404_response_from_server(mock_server):
    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/holds"),
                             Response(status_code=404)))

    with mock_server(imposter) as server:
        config = {
            'source_url': f"{imposter.url}/holds",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt'
        }
        job_config = CircrequestsJobConfig(config, 'test')

        query_source_url = QuerySourceUrl(job_config)

        step_result = query_source_url.execute()

        assert step_result.was_successful() is False
        assert_that(server, had_request().with_path("/holds").and_method("GET"))
        assert f"Retrieval of '{imposter.url}/holds' failed with a status code of 404" in \
               step_result.get_errors()


def test_server_does_not_exist():
    config = {
        'source_url': "http://localhost:12345/URL_DOES_NOT_EXIST",
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt'
    }
    job_config = CircrequestsJobConfig(config, 'test')

    query_source_url = QuerySourceUrl(job_config)

    with pytest.raises(requests.exceptions.ConnectionError):
        query_source_url.execute()
