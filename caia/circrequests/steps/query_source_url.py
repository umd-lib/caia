from caia.core.step import Step, StepResult
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
import requests
import logging
from typing import List

logger = logging.getLogger(__name__)


class QuerySourceUrl(Step):
    """
    Queries the source url and stores a successful response.
    """
    def __init__(self, job_config: CircrequestsJobConfig):
        self.job_config = job_config
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        source_url = self.job_config['source_url']
        logger.info(f"Querying {source_url}")

        headers = {'Content-Type': 'application/json'}
        request = requests.get(source_url, headers=headers)

        status_code = request.status_code
        logger.debug(f"request completed with status code: {status_code}")

        if status_code == requests.codes.ok:
            step_result = StepResult(True, request.text)
            return step_result
        else:
            error = f"Retrieval of '{source_url}' failed with a status code of {status_code}"
            self.errors.append(error)
            step_result = StepResult(False, request.text, self.errors)
            return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
