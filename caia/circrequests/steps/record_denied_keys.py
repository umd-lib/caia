import json
import logging
from typing import List

from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.core.step import Step, StepResult

logger = logging.getLogger(__name__)


class RecordDeniedKeys(Step):
    """
    Records the list of denied keys (if any).
    """
    def __init__(self, job_config: CircrequestsJobConfig, dest_response_body: str):
        self.job_config = job_config
        self.dest_response_body = dest_response_body
        self.errors: List[str] = []

    def execute(self) -> StepResult:
        dest_response = json.loads(self.dest_response_body)
        results = dest_response['results']
        denied_keys = []

        for result in results:
            denied = result['deny'] == "Y"
            if denied:
                denied_keys.append(result['item'])

        if denied_keys:
            logger.info(f"Denied key(s):")
            logger.info(denied_keys)

        # Always write out denied keys, even if there are none
        denied_keys_filepath = self.job_config['denied_keys_filepath']
        with open(denied_keys_filepath, "w") as fp:
            json.dump(denied_keys, fp)

        step_result = StepResult(True, denied_keys)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
