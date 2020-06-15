import argparse
import json
import logging
import os

import caia.core.command
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.steps.create_dest_request import CreateDestRequest
from caia.circrequests.steps.diff_against_last_success import DiffAgainstLastSuccess
from caia.circrequests.steps.query_source_url import QuerySourceUrl
from caia.circrequests.steps.record_denied_keys import RecordDeniedKeys
from caia.circrequests.steps.send_to_dest import SendToDest
from caia.circrequests.steps.update_last_success import UpdateLastSuccess
from caia.circrequests.steps.validate_job_preconditions import ValidateJobPreconditions
from caia.core.command import CommandResult
from caia.core.io import write_to_file
from caia.core.step import run_step

logger = logging.getLogger(__name__)


def configure_cli(subparsers) -> None:  # type: ignore
    """
    Configures the CLI arguments for this command
    """
    parser = subparsers.add_parser(
        name='circrequests',
        description='Retrieve hold requests from Aleph and send to CaiaSoft'
    )
    parser.set_defaults(cmd_name='circrequests')


def create_job_configuration(start_time: str) -> CircrequestsJobConfig:
    """
    Creates the new job configuration
    """
    # Create job configuration
    config = {
        'source_url': os.getenv("CIRCREQUESTS_SOURCE_URL", default=""),
        'dest_url': os.getenv("CIRCREQUESTS_DEST_URL", default=""),
        'caiasoft_api_key': os.getenv('CAIASOFT_API_KEY', default=""),
        'storage_dir': os.getenv('CIRCREQUESTS_STORAGE_DIR', default=""),
        'last_success_lookup': os.getenv('CIRCREQUESTS_LAST_SUCCESS_LOOKUP', default=""),
        'denied_keys_filepath': os.getenv('CIRCREQUESTS_DENIED_KEYS', default="")
    }

    job_id_prefix = "caia.circrequests"

    job_config = CircrequestsJobConfig(config, job_id_prefix, start_time)
    logger.info(f"Job Id: {job_config['job_id']}")
    logger.debug(f"job_config={job_config}")

    return job_config


class Command(caia.core.command.Command):
    def __call__(self, start_time: str, args: argparse.Namespace) -> caia.core.command.CommandResult:
        # Create job configuration
        job_config = create_job_configuration(start_time)

        # Validate preconditions
        step_result = run_step(ValidateJobPreconditions(job_config))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Query source URL
        step_result = run_step(QuerySourceUrl(job_config))
        write_to_file(job_config["source_response_body_filepath"], step_result.result)
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Diff against last success
        step_result = run_step(DiffAgainstLastSuccess(job_config))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        diff_result = step_result.get_result()

        # Write diff result to a file
        write_to_file(job_config['diff_result_filepath'], json.dumps(diff_result.as_dict()))

        if len(diff_result.new_entries) == 0:
            logger.info("No new entries found, no CaiaSoft update required.")
            # No new entries, so nothing to send to CaiaSoft
            # Record job as successful
            step_result = run_step(UpdateLastSuccess(job_config))
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Create POST body
        step_result = run_step(CreateDestRequest(job_config, diff_result))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Write POST request body to file
        write_to_file(job_config['dest_request_body_filepath'], step_result.get_result())

        # Send POST data to destination
        step_result = run_step(SendToDest(job_config))

        # Write dest response body to a file
        dest_response_body = step_result.get_result()
        write_to_file(job_config['dest_response_body_filepath'], dest_response_body)

        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Record denied keys (if any)
        step_result = run_step(RecordDeniedKeys(job_config, dest_response_body))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Record job as successful
        step_result = run_step(UpdateLastSuccess(job_config))
        return CommandResult(step_result.was_successful(), step_result.get_errors())
