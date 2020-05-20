import os
import glob
from invoke import task
from dotenv import load_dotenv


@task
def reset(c):
    """
    Resets application by removing "last_successful_lookup" file
    """
    load_dotenv()

    last_successful_lookup = os.getenv("CIRCREQUESTS_LAST_SUCCESS_LOOKUP") or ""
    if not last_successful_lookup:
        print("Aborting. CIRCREQUESTS_LAST_SUCCESS_LOOKUP is not set.")
        exit(1)

    if last_successful_lookup and os.path.exists(last_successful_lookup) and os.path.isfile(last_successful_lookup):
        os.remove(last_successful_lookup)


@task(reset)
def clean(c):
    """
    Cleans out all storage/circrequests directory and logs, and runs "reset"
    """
    load_dotenv()

    circrequests_storage_dir = os.getenv("CIRCREQUESTS_STORAGE_DIR")

    if not circrequests_storage_dir:
        print("Aborting. CIRCREQUESTS_STORAGE_DIR is not set.")
        exit(1)

    if circrequests_storage_dir and os.path.exists(circrequests_storage_dir):
        file_list = glob.glob(os.path.join(circrequests_storage_dir, '*.json'))
        for file_path in file_list:
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
