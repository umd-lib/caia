from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.steps.validate_job_preconditions import ValidateJobPreconditions


def test_validate_preconditions_returns_true_if_all_preconditions_are_met():
    config = {
        'caiasoft_api_key': 'SECRET_CAIASOFT_API_KEY',
        'source_url': 'http://example.com/source',
        'dest_url': 'http://example.org/dest',
        'log_dir': '/tmp/',
        'storage_dir': '/tmp/',
        'last_success_lookup': 'tests/storage/circrequests/circrequests_last_success.txt',
        'last_success_filepath': 'etc/circrequests_FIRST.json',
        'source_key_field': 'barcode'
    }

    job_config = CircrequestsJobConfig(config)

    validate_job_preconditions = ValidateJobPreconditions(job_config)
    step_result = validate_job_preconditions.execute()
    assert step_result.was_successful() is True
