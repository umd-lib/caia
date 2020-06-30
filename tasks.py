import glob
import os

from dotenv import load_dotenv
from invoke import task
from caia.circrequests.circrequests_job_config import get_last_success_filepath as circrequests_get_last_success_filepath  # noqa
from caia.items.items_job_config import get_last_success_filepath as items_get_last_success_filepath


@task
def clean_circrequests(c):
    """
    Cleans out all storage/circrequests directory and logs
    """
    load_dotenv()

    circrequests_storage_dir = os.getenv("CIRCREQUESTS_STORAGE_DIR")

    if not circrequests_storage_dir:
        print("Aborting. CIRCREQUESTS_STORAGE_DIR is not set.")
        exit(1)

    files_to_skip = []
    # Figure out which JSON file (if any) is used by the last success lookup,
    # so we don't delete it.
    circrequests_last_success_lookup = os.getenv("CIRCREQUESTS_LAST_SUCCESS_LOOKUP")
    last_success_filepath = None
    if os.path.exists(circrequests_last_success_lookup):
        last_success_filepath = circrequests_get_last_success_filepath(circrequests_last_success_lookup)
        files_to_skip.append(last_success_filepath)

    denied_keys = os.getenv("CIRCREQUESTS_DENIED_KEYS")
    if denied_keys and os.path.exists(denied_keys) and os.path.isfile(denied_keys):
        files_to_skip.append(denied_keys)

    if circrequests_storage_dir and os.path.exists(circrequests_storage_dir):
        file_list = glob.glob(os.path.join(circrequests_storage_dir, '*.json'))
        for file_path in file_list:
            # Skip file if in files_to_skip
            if file_path in files_to_skip:
                continue
            try:
                os.remove(file_path)
            except Exception:
                print("Error while deleting file : ", file_path)

    log_dir = os.getenv("LOG_DIR")

    if not log_dir:
        print("Aborting. CIRCREQUESTS_STORAGE_DIR is not set.")
        exit(1)

    if log_dir and os.path.exists(log_dir):
        file_list = glob.glob(os.path.join(log_dir, '*.log'))
        for file_path in file_list:
            try:
                os.remove(file_path)
            except Exception:
                print("Error while deleting file : ", file_path)


@task
def clean_items(c):
    """
    Cleans out all storage/items directory
    """
    load_dotenv()

    items_storage_dir = os.getenv("ITEMS_STORAGE_DIR")

    if not items_storage_dir:
        print("Aborting. ITEMS_STORAGE_DIR is not set.")
        exit(1)

    # Figure out which JSON file (if any) is used by the last success lookup,
    # so we don't delete it.
    item_last_success_lookup = os.getenv("ITEMS_LAST_SUCCESS_LOOKUP")
    last_success_filepath = None
    if os.path.exists(item_last_success_lookup):
        last_success_filepath = items_get_last_success_filepath(item_last_success_lookup)

    if items_storage_dir and os.path.exists(items_storage_dir):
        file_list = glob.glob(os.path.join(items_storage_dir, '*.json'))
        for file_path in file_list:
            # Skip the last_success_filepath
            if last_success_filepath and file_path == last_success_filepath:
                continue
            try:
                os.remove(file_path)
            except Exception:
                print("Error while deleting file : ", file_path)


@task
def clean_logs(c):
    """
    Cleans out the logs directory
    """
    log_dir = os.getenv("LOG_DIR")

    if not log_dir:
        print("Aborting. LOG_DIR is not set.")
        exit(1)

    if log_dir and os.path.exists(log_dir):
        file_list = glob.glob(os.path.join(log_dir, '*.log'))
        for file_path in file_list:
            try:
                os.remove(file_path)
            except Exception:
                print("Error while deleting file : ", file_path)


@task(clean_circrequests, clean_items, clean_logs)
def clean(c):
    """
    Cleans out storage
    """


@task
def reset_circrequests(c):
    """
    Resets circrequests by removing "last_successful_lookup" and denied keys file
    """
    load_dotenv()

    last_successful_lookup = os.getenv("CIRCREQUESTS_LAST_SUCCESS_LOOKUP") or ""
    if not last_successful_lookup:
        print("Aborting. CIRCREQUESTS_LAST_SUCCESS_LOOKUP is not set.")
        exit(1)

    if last_successful_lookup and os.path.exists(last_successful_lookup) and os.path.isfile(last_successful_lookup):
        os.remove(last_successful_lookup)

    denied_keys = os.getenv("CIRCREQUESTS_DENIED_KEYS") or ""
    if not denied_keys:
        print("Aborting. CIRCREQUESTS_DENIED_KEYS is not set.")
        exit(1)

    if denied_keys and os.path.exists(denied_keys) and os.path.isfile(denied_keys):
        os.remove(denied_keys)


@task
def reset_items(c):
    """
    Resets items by removing "last_successful_lookup" file
    """
    load_dotenv()

    last_successful_lookup = os.getenv("ITEMS_LAST_SUCCESS_LOOKUP") or ""
    if not last_successful_lookup:
        print("Aborting. ITEMS_LAST_SUCCESS_LOOKUP is not set.")
        exit(1)

    if last_successful_lookup and os.path.exists(last_successful_lookup) and os.path.isfile(last_successful_lookup):
        os.remove(last_successful_lookup)


@task(reset_circrequests, reset_items)
def reset(c):
    """
    Removed the "last success" file for circrequests and items
    """


@task(reset, clean)
def reset_and_clean(c):
    """
    Performs a "reset" and "clean", ensuring they are done in the proper order.
    """
