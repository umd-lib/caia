import datetime
import json
import logging
from typing import cast, Dict, List

from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.core.step import Step, StepResult
from caia.circrequests.diff import DiffResult

logger = logging.getLogger(__name__)


class RecordDeniedKeys(Step):
    """
    Records the list of denied keys (if any).
    """
    def __init__(self, job_config: CircrequestsJobConfig, dest_response_body: str,
                 current_time: datetime.datetime, diff_result: DiffResult):
        self.job_config = job_config
        self.dest_response_body = dest_response_body
        self.current_time = current_time
        self.diff_result = diff_result
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

        denied_keys_to_persist = cast(Dict[str, str], self.diff_result.as_dict()['denied_keys_to_persist'])
        # Add any new denied keys to denied_keys_to_persist
        for denied_key in denied_keys:
            denied_keys_to_persist[denied_key] = self.current_time.isoformat()

        # Always write out denied keys, even if there are none
        denied_keys_filepath = self.job_config['denied_keys_filepath']
        with open(denied_keys_filepath, "w") as fp:
            json.dump(denied_keys_to_persist, fp)

        step_result = StepResult(True, denied_keys_to_persist)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
