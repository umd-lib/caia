import datetime
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.steps.diff_against_last_success import DiffAgainstLastSuccess


def test_diff_against_last_success():
    config = {
        'last_success_filepath': 'tests/resources/circrequests/valid_src_response_with_no_entries.json',
        'storage_dir': '/tmp',
        'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt',
        'denied_keys_filepath': 'tests/storage/circrequests/circrequests_denied_keys.json',
        'denied_items_wait_interval': '604800'
    }

    job_config = CircrequestsJobConfig(config, 'test')
    # Override "source_response_body_filepath" in job config
    job_config['source_response_body_filepath'] = 'tests/resources/circrequests/valid_src_response.json'

    current_time = datetime.datetime.now
    diff_against_last_success = DiffAgainstLastSuccess(job_config, current_time)

    step_result = diff_against_last_success.execute()
    assert step_result.was_successful() is True

    diff_result = step_result.get_result()

    assert len(diff_result.new_entries) == 1
