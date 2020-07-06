import logging
from typing import List

from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.core.http import http_get_request
from caia.core.step import Step, StepResult

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
        headers = {'Content-Type': 'application/json'}

        return http_get_request(source_url, headers)

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
