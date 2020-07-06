import caia.core.assertions as assertions
from caia.core.job_config import JobConfig


def test_assert_key_exists():
    config = {
        'key_with_none': None,
        'key_with_string': 'string'
    }
    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_key_exists(job_config, 'key_with_none', errors) is True
    assert assertions.assert_key_exists(job_config, 'key_with_string', errors) is True
    assert len(errors) == 0
    assert assertions.assert_key_exists(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_value_not_none():
    config = {
        'key_with_string': 'string',
        'key_with_empty_string': '',
        'key_with_none': None,
    }

    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_value_not_none(job_config, 'key_with_string', errors) is True
    assert assertions.assert_value_not_none(job_config, 'key_with_empty_string', errors) is True
    assert len(errors) == 0
    assert assertions.assert_value_not_none(job_config, 'key_with_none', errors) is False
    assert "'key_with_none' has a value of None" in errors
    assert assertions.assert_value_not_none(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_nonempty_value():
    config = {
        'key_with_none': None,
        'key_with_empty_string': '',
        'key_with_only_whitespace': '   \t  ',
        'key_with_value': 'value',
    }
    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_nonempty_value(job_config, 'key_with_value', errors) is True
    assert len(errors) == 0
    assert assertions.assert_nonempty_value(job_config, 'key_with_none', errors) is False
    assert "'key_with_none' has a value of None" in errors
    assert assertions.assert_nonempty_value(job_config, 'key_with_empty_string', errors) is False
    assert "'key_with_empty_string' has an empty value" in errors
    assert assertions.assert_nonempty_value(job_config, 'key_with_only_whitespace', errors) is False
    assert "'key_with_only_whitespace' has an empty value" in errors
    assert assertions.assert_nonempty_value(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_is_non_negative_integer():
    config = {
        # Allowed value
        'key_with_integer_value': '1234',
        'key_with_zero_value': '0',
        # Disallowed values
        'key_with_negative_integer_value': '-1234',
        'key_with_none': None,
        'key_with_empty_string': '',
        'key_with_only_whitespace': '   \t  ',
        'key_with_string_value': 'value',
        'key_with_float_value': '1234.45',
    }
    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_integer_value', errors) is True
    assert len(errors) == 0
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_zero_value', errors) is True
    assert len(errors) == 0
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_negative_integer_value', errors) is False
    assert "'key_with_negative_integer_value' is not a non-negative integer." in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_float_value', errors) is False
    assert "'key_with_float_value' is not a non-negative integer." in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_string_value', errors) is False
    assert "'key_with_string_value' is not a non-negative integer." in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_none', errors) is False
    assert "'key_with_none' has a value of None" in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_empty_string', errors) is False
    assert "'key_with_empty_string' is not a non-negative integer." in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'key_with_only_whitespace', errors) is False
    assert "'key_with_only_whitespace' is not a non-negative integer." in errors
    assert assertions.assert_is_non_negative_integer(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_directory_exists():
    config = {
        'dir_exists': '/tmp/',
        'dir_none': None,
        'dir_empty': '',
        'dir_does_not_exist': '/dir-does-not-exist/'
    }

    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_directory_exists(job_config, 'dir_exists', errors) is True
    assert len(errors) == 0
    assert assertions.assert_directory_exists(job_config, 'dir_none', errors) is False
    assert "'dir_none' has a value of None" in errors
    assert assertions.assert_directory_exists(job_config, 'dir_empty', errors) is False
    assert "'dir_empty' has an empty value" in errors
    assert assertions.assert_directory_exists(job_config, 'dir_does_not_exist', errors) is False
    assert "'dir_does_not_exist': '/dir-does-not-exist/' does not exist" in errors
    assert assertions.assert_directory_exists(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_valid_url():
    config = {
        'url_valid': 'https://www.lib.umd.edu/',
        'url_none': None,
        'url_empty': '',
        'url_invalid': 'foobarbazquuz123'
    }

    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_valid_url(job_config, 'url_valid', errors) is True
    assert len(errors) == 0
    assert assertions.assert_valid_url(job_config, 'url_none', errors) is False
    assert "'url_none' has a value of None" in errors
    assert assertions.assert_valid_url(job_config, 'url_empty', errors) is False
    assert "'url_empty' has an empty value" in errors
    assert assertions.assert_valid_url(job_config, 'url_invalid', errors) is False
    assert "'url_invalid': 'foobarbazquuz123' is not a valid URL" in errors
    assert assertions.assert_valid_url(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_file_exists():
    config = {
        'file_exists': 'requirements.txt',
        'file_does_not_exist': '/nonexistent_directory/nonexistent_file.txt',
        'file_is_empty': '',
        'file_is_none': None
    }

    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_file_exists(job_config, 'file_exists', errors) is True
    assert len(errors) == 0
    assert assertions.assert_file_exists(job_config, 'file_does_not_exist', errors) is False
    assert "'/nonexistent_directory/nonexistent_file.txt' does not exist" in errors
    assert assertions.assert_file_exists(job_config, 'file_is_empty', errors) is False
    assert "'file_is_empty' has an empty value" in errors
    assert assertions.assert_valid_url(job_config, 'file_is_none', errors) is False
    assert "'file_is_none' has a value of None" in errors
    assert assertions.assert_file_exists(job_config, 'nonexistent_key', errors) is False
    assert "'nonexistent_key' is missing" in errors


def test_assert_valid_json_file():
    config = {
        'valid_json_file': 'tests/resources/circrequests/valid_src_response.json',
        'invalid_json_file': 'tests/resources/circrequests/sample_file.csv'
    }

    job_config = JobConfig(config)

    errors = []
    assert assertions.assert_valid_json_file(job_config, 'valid_json_file', errors) is True
    assert len(errors) == 0
    assert assertions.assert_valid_json_file(job_config, 'invalid_json_file', errors) is False
    assert "'tests/resources/circrequests/sample_file.csv' is not a parseable JSON file" in errors
