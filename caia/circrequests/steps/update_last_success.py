from caia.core.step import Step, StepResult
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig, generate_storage_filepath


class UpdateLastSuccess(Step):
    """
    Validates that all preconditions necessary for the job have been met.
    """
    def __init__(self, job_config: CircrequestsJobConfig):
        self.job_config = job_config
        self.errors = []

    def execute(self) -> StepResult:
        last_success_lookup = self.job_config['last_success_lookup']

        last_success_filepath = generate_storage_filepath(self.job_config, "source_response_body", "json")
        self.job_config['last_success_filepath'] = last_success_filepath
        with open(last_success_lookup, "w") as fp:
            last_success = self.job_config['last_success_filepath']
            fp.write(last_success)

        step_result = StepResult(True, None)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"