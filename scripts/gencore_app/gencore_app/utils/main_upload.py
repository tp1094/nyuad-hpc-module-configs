import logging
import sys
from gencore_app.utils.main import run_command
from gencore_app.utils.main_env import from_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def upload_remote_env(fname, verbose=False):

    #TODO Update this to use conda env upload utils
    logging.info("Uploading remote env of {}".format(fname))
    env = from_file(fname)
    env.save()
    cmd = "conda env upload -f {}".format(fname)
    return run_command(cmd, verbose)

def status_check_upload(upload_env_passes):

    if not upload_env_passes:
        logging.info("One or more uploads failed!")
        sys.exit(1)
    else:
        logging.info("Upload passed!")
