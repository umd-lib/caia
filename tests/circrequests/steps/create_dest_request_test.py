from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.diff import DiffResult
from caia.circrequests.steps.create_dest_request import CreateDestRequest


def test_create_dest_request():
    config = {
        'last_success_filepath': 'tests/resources/circrequests/valid_src_response_with_no_entries.json',
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt',
        'denied_keys_filepath': 'tests/storage/circrequests/circrequests_denied_keys.json'
    }

    job_config = CircrequestsJobConfig(config, 'test')

    new_entries = [{"barcode": "31430023550355", "stop": "CPMCK", "patron_id": "000000224432"}]

    diff_result = DiffResult(new_entries, [], [])
    create_dest_request = CreateDestRequest(job_config, diff_result)

    step_result = create_dest_request.execute()
    assert step_result.was_successful() is True

    expected_request_body = \
        '{"requests": [{"barcode": "31430023550355", "request_type": "PYR", ' \
        '"patron_id": "000000224432"}]}'
    assert expected_request_body == step_result.get_result()
