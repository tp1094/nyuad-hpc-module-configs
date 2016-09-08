import logging
import sys
from gencore_app.utils.main import run_command

logging.basicConfig(level=logging.DEBUG)

def upload_remote_env(fname, verbose=False):

    #TODO Update this to use conda env upload utils
    logging.debug("Uploading remote env of {}".format(fname))
    cmd = "conda env upload -f {}".format(fname)
    return run_command(cmd, verbose)

def status_check_upload(upload_env_passes):

    if not upload_env_passes:
        logging.warn("One or more uploads failed!")
        sys.exit(1)
    else:
        logging.info("Upload passed!")
