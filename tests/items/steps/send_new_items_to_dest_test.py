from hamcrest import assert_that
import tempfile

from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.matchers import had_request

from caia.items.items_job_config import ItemsJobConfig
from caia.items.steps.send_new_items_to_dest import SendNewItemsToDest


def test_send_new_items_to_dest_valid_response(mock_server):
    with open("tests/resources/items/valid_dest_new_items_response.json") as file:
        valid_dest_response = file.read()

    # Set up mock server with required behavior
    imposter = Imposter(Stub(Predicate(path="/items/incoming", method="POST"),
                             Response(body=valid_dest_response)))

    with mock_server(imposter) as server:
        config = {
            'dest_new_url': f"{imposter.url}/items/incoming",
            'storage_dir': '/tmp',
            'last_success_lookup': 'tests/storage/items/items_last_success.txt',
            'caiasoft_api_key': "SOME_SECRET_KEY"
        }
        job_config = ItemsJobConfig(config, 'test')
        # Override dest_new_items_request_body_filepath
        job_config["dest_new_items_request_body_filepath"] = "tests/resources/items/valid_dest_new_items_request.json"
        with tempfile.TemporaryDirectory() as temp_storage_dir:
            job_config["dest_new_items_response_body_filepath"] = temp_storage_dir + "/dest_new_items_response.json"

            send_new_items_to_dest = SendNewItemsToDest(job_config)
            step_result = send_new_items_to_dest.execute()

            assert step_result.was_successful() is True
            assert_that(server, had_request().with_path("/items/incoming").and_method("POST"))
            assert valid_dest_response == step_result.get_result()
