from caia.items.items_job_config import ItemsJobConfig
from caia.items.steps.validate_job_preconditions import ValidateJobPreconditions


def test_validate_preconditions_returns_true_if_all_preconditions_are_met():
    config = {
        'caiasoft_api_key': 'SECRET_CAIASOFT_API_KEY',
        'source_url': 'http://example.com/source',
        'dest_new_url': 'http://example.org/dest/incoming',
        'dest_updates_url': 'http://example.org/dest/updates',
        'log_dir': '/tmp/',
        'storage_dir': '/tmp/',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt',
        'last_success_filepath': 'etc/items_FIRST.json',
    }

    job_config = ItemsJobConfig(config)

    validate_job_preconditions = ValidateJobPreconditions(job_config)
    step_result = validate_job_preconditions.execute()
    assert step_result.was_successful() is True


def test_validate_preconditions_returns_false_if_some_preconditions_are_not_met():
    config = {
        # Missing 'caiasoft_api_key'
        'source_url': 'http://example.com/source',
        'dest_new_url': 'http://example.org/dest/incoming',
        'dest_updates_url': 'http://example.org/dest/updates',
        'log_dir': '/tmp/',
        'storage_dir': '/tmp/',
        'last_success_lookup': 'tests/storage/items/items_last_success.txt',
        'last_success_filepath': 'etc/items_FIRST.json',
    }

    job_config = ItemsJobConfig(config)

    validate_job_preconditions = ValidateJobPreconditions(job_config)
    step_result = validate_job_preconditions.execute()
    assert step_result.was_successful() is False
