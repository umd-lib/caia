import os
import uuid
from typing import Dict, Any
from datetime import datetime
import yaml


class JobConfig(Dict[str, str]):
    """
    Contains all the configuration parameters for a job, including the job id.
    """
    def __init__(self, config: Dict[str, str], job_id_prefix: str = '', timestamp: str = ""):
        super().__init__()
        if not timestamp:
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

        self['job_id'] = JobIdGenerator.create_id(job_id_prefix, timestamp)

        # Import YAML configuration file
        application_config_file = "etc/config.yaml"
        with open(application_config_file) as f:
            self.__application_config = yaml.load(f, Loader=yaml.FullLoader)

        self.update(config)

    @property
    def application_config(self) -> Any:
        return self.__application_config

    def generate_filepath(self, base_dir: str, file_descriptor: str, file_extension: str) -> str:
        """
        Returns a fully qualified filepath, based one this JobConfig, and
        the given base directory, file descriptor, and extension
        """
        job_id = self['job_id']

        base_filename = f"{job_id}.{file_descriptor}.{file_extension}"
        return os.path.join(base_dir, base_filename)

    def __str__(self) -> str:
        """
        Returns a string representation of this object.
        """
        str_prefix = f"JobConfig@{id(self)}[job_id: {self['job_id']}', "

        key_values = []
        for key in self.keys():
            if key == 'job_id':
                continue
            if key != 'caiasoft_api_key':
                key_values.append(f"{key}: {self[key]}")
            else:
                key_values.append(f"{key}: [REDACTED]")

        keys_str = ', '.join(key_values)

        return str_prefix + keys_str


class JobIdGenerator:
    """
    Generates unique job ids
    """
    @staticmethod
    def create_id(job_id_prefix: str, timestamp: str) -> str:
        """
        Returns a unique job id consisting of the give job prefix, timestamp
        and a generated UUID.
        """
        uid = uuid.uuid4()
        job_id = f"{job_id_prefix}.{timestamp}-{uid}"
        return job_id
