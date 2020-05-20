from typing import Dict
from caia.core.job_config import JobConfig
import os
import logging

logger = logging.getLogger(__name__)


def generate_storage_filepath(job_config: JobConfig, file_descriptor: str, file_extension: str) -> str:
    """
    Returns a fully qualified filepath, based the given JobConfig,
    file descriptor, and extension
    """
    job_id = job_config['job_id']
    storage_dir = job_config['storage_dir']

    base_filename = f"{job_id}.{file_descriptor}.{file_extension}"
    return os.path.join(storage_dir, base_filename)


def get_last_success_filepath(last_success_lookup: str) -> str:
    """
    Returns the filepath containing the last successful source response
    """
    with open(last_success_lookup) as fp:
        last_success_filepath = fp.readline().strip()
        return last_success_filepath


class CircrequestsJobConfig(JobConfig):
    def __init__(self, config: Dict[str, str], job_id_prefix: str = '', timestamp: str = None):
        super().__init__(config, job_id_prefix, timestamp)

        source_response_body_filepath = generate_storage_filepath(self, "source_response_body", "json")
        self['source_response_body_filepath'] = source_response_body_filepath

        diff_result_filepath = generate_storage_filepath(self, "diff_result", "json")
        self['diff_result_filepath'] = diff_result_filepath

        dest_request_body_filepath = generate_storage_filepath(self, "dest_request_body", "json")
        self['dest_request_body_filepath'] = dest_request_body_filepath

        dest_response_body_filepath = generate_storage_filepath(self, "dest_response_body", "json")
        self['dest_response_body_filepath'] = dest_response_body_filepath

        # Use "last_success_lookup" to populate the "last_success_filepath"
        # value, which is the actual JSON file to use in the "diff" comparison
        # against the result of the current job. If the "last_success_lookup"
        # file does not exist, create one, with "storage/etc/circrequests_FIRST.json"
        # as the JSON file it points to.
        if self['last_success_lookup']:
            last_success_lookup_filepath = self['last_success_lookup']
            if not os.path.exists(last_success_lookup_filepath):
                logger.warning(f"last_success_lookup file at '{last_success_lookup_filepath} was not found. "
                               "Creating default.")
                with open(last_success_lookup_filepath, "w") as fp:
                    fp.write("storage/etc/circrequests_FIRST.json")

        last_success_lookup = config['last_success_lookup']
        self["last_success_filepath"] = get_last_success_filepath(last_success_lookup)
