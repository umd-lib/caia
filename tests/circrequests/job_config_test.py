from datetime import datetime
from caia.core.job_config import JobConfig
from caia.core.job_config import JobIdGenerator


def test_job_id_generator_generates_unique_ids():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    job_id1 = JobIdGenerator.create_id('test', timestamp)
    job_id2 = JobIdGenerator.create_id('test', timestamp)
    assert job_id1 != job_id2


def test_job_configs_are_created_with_unique_ids():
    config = {
        'caiasoft_api_key': 'SECRET_CAIASOFT_API_KEY',
        'source_url': 'http://example.com/source',
        'dest_url': 'http://example.org/dest',
        'source_response_dir': '/tmp/source_response/',
        'diff_result_dir': '/tmp/diff_result/',
        'dest_request_dir': '/tmp/dest_request_dir/',
        'dest_response_dir': '/tmp/dest_response_dir/',
        'log_dir': '/tmp/log_dir/'
    }

    job_config1 = JobConfig(config)
    job_config2 = JobConfig(config)
    assert job_config1 != job_config2
    assert job_config1['job_id'] != job_config2['job_id']


def test_job_config_contains_all_config_keys():
    config = {
        'caiasoft_api_key': 'SECRET_CAIASOFT_API_KEY',
        'source_url': 'http://example.com/source',
        'dest_url': 'http://example.org/dest',
        'source_response_dir': '/tmp/source_response/',
        'diff_result_dir': '/tmp/diff_result/',
        'dest_request_dir': '/tmp/dest_request_dir/',
        'dest_response_dir': '/tmp/dest_response_dir/',
        'log_dir': '/tmp/log_dir/'
    }

    job_config = JobConfig(config)

    for key in config.keys():
        assert job_config[key] == config[key]
        assert job_config[key] == config[key]


def test_job_to_string():
    config = {
        'caiasoft_api_key': 'SECRET_CAIASOFT_API_KEY',
        'source_url': 'http://example.com/source',
        'dest_url': 'http://example.org/dest',
        'source_response_dir': '/tmp/source_response/',
        'diff_result_dir': '/tmp/diff_result/',
        'dest_request_dir': '/tmp/dest_request_dir/',
        'dest_response_dir': '/tmp/dest_response_dir/',
        'log_dir': '/tmp/log_dir/'
    }

    job_config = JobConfig(config)
    job_str = job_config.__str__()

    for key in config.keys():
        if key != 'caiasoft_api_key':
            expected_value = f"{key}: {config[key]}"
        else:
            expected_value = 'caiasoft_api_key: [REDACTED]'

        assert expected_value in job_str
