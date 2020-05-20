from caia.core.step import Step, StepResult
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
import caia.circrequests.assertions as assertions
from typing import List


class ValidateJobPreconditions(Step):
    """
    Validates that all preconditions necessary for the job have been met.
    """
    def __init__(self, job_config: CircrequestsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        # Verify CaiaSoft API key is present
        has_caiasoft_api_key = assertions.assert_nonempty_value(self.job_config, 'caiasoft_api_key', self.errors)

        has_source_url = assertions.assert_valid_url(self.job_config, "source_url", self.errors)
        has_dest_url = assertions.assert_valid_url(self.job_config, "dest_url", self.errors)

        has_storage_dir = assertions.assert_directory_exists(self.job_config, 'storage_dir', self.errors)

        has_last_success_lookup = assertions.assert_file_exists(self.job_config, "last_success_lookup", self.errors)
        has_last_success_filepath = assertions.assert_file_exists(self.job_config, "last_success_filepath", self.errors)

        has_source_key_field = assertions.assert_nonempty_value(self.job_config, 'source_key_field', self.errors)

        result = has_caiasoft_api_key and has_source_url and has_dest_url and has_storage_dir and \
            has_last_success_lookup and has_last_success_filepath and has_source_key_field

        step_result = StepResult(result, None, self.errors)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
