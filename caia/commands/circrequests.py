import caia.core.command
import argparse
import json
import os
from caia.circrequests.circrequests_job_config import CircrequestsJobConfig
from caia.circrequests.steps.validate_job_preconditions import ValidateJobPreconditions
from caia.circrequests.steps.query_source_url import QuerySourceUrl
from caia.circrequests.steps.diff_against_last_success import DiffAgainstLastSuccess
from caia.circrequests.steps.update_last_success import UpdateLastSuccess
from caia.circrequests.steps.send_to_dest import SendToDest
from caia.circrequests.diff import DiffResult
from caia.core.command import CommandResult
import logging
from typing import Any, Dict, Optional
from caia.core.step import Step, StepResult

logger = logging.getLogger(__name__)


def configure_cli(subparsers) -> None:
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
        'source_url': os.getenv("CIRCREQUESTS_SOURCE_URL"),
        'dest_url': os.getenv("CIRCREQUESTS_DEST_URL"),
        'caiasoft_api_key': os.getenv('CAIASOFT_API_KEY'),
        'storage_dir': os.getenv('CIRCREQUESTS_STORAGE_DIR'),
        'source_key_field': os.getenv('CIRCREQUESTS_SOURCE_KEY_FIELD'),
        'last_success_lookup': os.getenv('CIRCREQUESTS_LAST_SUCCESS_LOOKUP')
    }

    job_id_prefix = "caia.circrequests"

    job_config = CircrequestsJobConfig(config, job_id_prefix, start_time)
    logger.info(f"Job Id: {job_config['job_id']}")
    logger.debug(f"job_config={job_config}")

    return job_config


def from_json_file(filepath: str) -> Any:
    """
    Converts the JSON in the given filepath to Python
    """
    with open(filepath) as fp:
        return json.load(fp)


def dest_post_entry(request_id: Optional[str], diff_result_entry: Dict[str, str], source_key_field: str) \
        -> Dict[str, str]:
    """
    Converts a single diff result entry into a format suitable for the
    CaiaSoft.
    """
    post_entry = {
        "barcode": diff_result_entry[source_key_field],
        "request_type": "PYR",
        "stop": "McKeldin"
    }

    if request_id:
        post_entry['request_id'] = request_id

    return post_entry


def dest_post_request_body(diff_result: DiffResult, source_key_field: str) -> str:
    """
    Returns the JSON to send to CaiaSoft from the given DiffResult
    """

    requests = []
    for entry in diff_result.new_entries:
        request_id = None
        requests.append(dest_post_entry(request_id, entry, source_key_field))

    request_body = {"requests": requests}
    json_str = json.dumps(request_body)
    return json_str


def write_to_file(filepath: str, contents: str) -> None:
    """
    Writes the given string to the given filepath
    """
    with open(filepath, "w") as fp:
        fp.write(contents)


def run_step(step: Step) -> StepResult:
    """
    Runs a step
    """
    logger.debug(f"Starting {step}")
    step_result = step.execute()
    logger.debug(f"Completed {step} with result: {step_result}")
    return step_result


class Command(caia.core.command.Command):
    def __call__(self, start_time: str, args: argparse.Namespace) -> caia.core.command.CommandResult:
        # Create job configuration
        job_config = create_job_configuration(start_time)

        # Validate preconditions
        step_result = run_step(ValidateJobPreconditions(job_config))
        if not step_result.was_successful:
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Query source URL
        step_result = run_step(QuerySourceUrl(job_config))
        write_to_file(job_config["source_response_body_filepath"], step_result.result)
        if not step_result.was_successful:
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Diff against last success
        step_result = run_step(DiffAgainstLastSuccess(job_config))
        if not step_result.was_successful:
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

        # Create POST body, and store in a file
        request_body = dest_post_request_body(diff_result, job_config['source_key_field'])
        write_to_file(job_config['dest_request_body_filepath'], request_body)

        # Send POST data to destination
        step_result = run_step(SendToDest(job_config))

        # Write dest response body to a file
        write_to_file(job_config['dest_response_body_filepath'], step_result.get_result())

        if not step_result.was_successful:
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Record job as successful
        step_result = run_step(UpdateLastSuccess(job_config))
        return CommandResult(step_result.was_successful(), step_result.get_errors())
