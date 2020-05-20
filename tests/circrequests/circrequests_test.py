import requests
from hamcrest import assert_that
from brunns.matchers.response import is_response
from mbtest.matchers import had_request
from mbtest.imposters import Imposter, Predicate, Response, Stub


def test_request_to_mock_server(mock_server):

    with open("tests/resources/circrequests/valid_dest_request.json") as file:
        valid_json_request = file.read()

    with open("tests/resources/circrequests/valid_dest_response.json") as file:
        valid_json_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/api/circrequests/v1"),
                             Response(body=valid_json_response)))

    with mock_server(imposter) as server:
        # Make request to mock server - exercise code under test here
        response = requests.post("{}/api/circrequests/v1".format(imposter.url),
                                 data=valid_json_request)

        assert_that(response,
                    is_response().with_status_code(200).and_body(valid_json_response))
        assert_that(server, had_request().with_path("/api/circrequests/v1").and_method("POST"))
