import argparse
import logging
import os
from datetime import datetime

import caia.core.command
from caia.core.command import CommandResult
from caia.core.io import write_to_file
from caia.core.step import run_step
from caia.items.items_job_config import ItemsJobConfig
from caia.items.steps.create_dest_request import CreateDestNewItemsRequest
from caia.items.steps.create_dest_request import CreateDestUpdatedItemsRequest
from caia.items.steps.get_last_timestamp import GetLastTimestamp
from caia.items.steps.parse_source_response import ParseSourceResponse
from caia.items.steps.query_source_url import QuerySourceUrl
from caia.items.steps.send_new_items_to_dest import SendNewItemsToDest
from caia.items.steps.send_updated_items_to_dest import SendUpdatedItemsToDest
from caia.items.steps.update_last_success import UpdateLastSuccess
from caia.items.steps.validate_job_preconditions import ValidateJobPreconditions

logger = logging.getLogger(__name__)


def configure_cli(subparsers) -> None:  # type: ignore
    """
    Configures the CLI arguments for this command
    """
    parser = subparsers.add_parser(
        name='items',
        description='Retrieve new/updated items from Aleph and send to CaiaSoft'
    )
    parser.set_defaults(cmd_name='items')


def create_job_configuration(start_time: str) -> ItemsJobConfig:
    """
    Creates the new job configuration
    """
    # Create job configuration
    config = {
        'source_url': os.getenv("ITEMS_SOURCE_URL", default=""),
        'dest_new_url': os.getenv("ITEMS_DEST_NEW_URL", default=""),
        'dest_updates_url': os.getenv("ITEMS_DEST_UPDATES_URL", default=""),
        'caiasoft_api_key': os.getenv('CAIASOFT_API_KEY', default=""),
        'storage_dir': os.getenv('ITEMS_STORAGE_DIR', default=""),
        'last_success_lookup': os.getenv('ITEMS_LAST_SUCCESS_LOOKUP', default="")
    }

    job_id_prefix = "caia.items"

    job_config = ItemsJobConfig(config, job_id_prefix, start_time)
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

        # Get the last timestamp
        step_result = run_step(GetLastTimestamp(job_config))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        last_timestamp = step_result.get_result()

        # Query source URL
        now = datetime.now()
        current_timestamp = now.strftime("%Y%m%d%H%M%S")
        step_result = run_step(QuerySourceUrl(job_config, last_timestamp, current_timestamp))
        write_to_file(job_config["source_response_body_filepath"], step_result.result)
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        source_response = step_result.get_result()

        # Parse source response
        step_result = run_step(ParseSourceResponse(source_response))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        source_items = step_result.get_result()

        # Create new items POST body
        step_result = run_step(CreateDestNewItemsRequest(source_items))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Write new items request body to file
        write_to_file(job_config['dest_new_items_request_body_filepath'], step_result.get_result())

        # Send POST new items data to destination
        step_result = run_step(SendNewItemsToDest(job_config))

        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Write new items dest response body to a file
        write_to_file(job_config['dest_new_items_response_body_filepath'], step_result.get_result())

        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Create updated items POST body
        step_result = run_step(CreateDestUpdatedItemsRequest(source_items))
        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Write updated items request body to file
        write_to_file(job_config['dest_updated_items_request_body_filepath'], step_result.get_result())

        # Send POST updated items data to destination
        step_result = run_step(SendUpdatedItemsToDest(job_config))

        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Write updated items dest response body to a file
        write_to_file(job_config['dest_updated_items_response_body_filepath'], step_result.get_result())

        if not step_result.was_successful():
            return CommandResult(step_result.was_successful(), step_result.get_errors())

        # Record job as successful
        step_result = run_step(UpdateLastSuccess(job_config))
        return CommandResult(step_result.was_successful(), step_result.get_errors())
