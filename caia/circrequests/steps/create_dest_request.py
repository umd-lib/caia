import json
import logging
from typing import Dict, List, Optional

from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.diff import DiffResult
from caia.core.step import Step, StepResult

logger = logging.getLogger(__name__)


class CreateDestRequest(Step):
    """
    Constructs the POST request body to send to the destination
    """
    def __init__(self, job_config: CircrequestsJobConfig, diff_result: DiffResult):
        self.job_config = job_config
        self.diff_result = diff_result
        self.errors: List[str] = []

    @staticmethod
    def dest_post_entry(request_id: Optional[str], diff_result_entry: Dict[str, str],
                        source_key_field: str, library_stops: Dict[str, str]) -> Dict[str, str]:
        """
        Converts a single diff result entry into a format suitable for the
        CaiaSoft.
        """
        aleph_library_location = diff_result_entry["stop"]
        caiasoft_library_stop = library_stops[aleph_library_location]
        post_entry = {
            "barcode": diff_result_entry[source_key_field],
            "request_type": "PYR",
            "stop": caiasoft_library_stop
        }

        if request_id:
            post_entry['request_id'] = request_id

        return post_entry

    @staticmethod
    def dest_post_request_body(diff_result: DiffResult, source_key_field: str,
                               library_stops: Dict[str, str]) -> str:
        """
        Returns the JSON to send to CaiaSoft from the given DiffResult
        """

        requests = []
        for entry in diff_result.new_entries:
            request_id = None
            post_entry = CreateDestRequest.dest_post_entry(request_id, entry, source_key_field, library_stops)
            requests.append(post_entry)

        request_body = {"requests": requests}
        json_str = json.dumps(request_body)
        return json_str

    def execute(self) -> StepResult:
        source_key_field = self.job_config.application_config['circrequests']['source_key_field']
        library_stops = self.job_config.application_config['library_stops']

        request_body = self.dest_post_request_body(self.diff_result, source_key_field, library_stops)
        step_result = StepResult(True, request_body)
        return step_result

    def __str__(self) -> str:
        fullname = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return f"{fullname}@{id(self)}"
