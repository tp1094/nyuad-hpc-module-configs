import logging
import sys
# from conda_env import env
# import os
from click_test.utils.main import run_command

# from binstar_client.utils import get_server_api
# aserver_api = get_server_api()

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
        logging.info("All uploads passed!")
        sys.exit(0)


# def loop_files_build(tfile):
    # """ Make sure the env builds """

    # create_env_passes = False

    # create_env_passes = try_conda_env_create(tfile)

    # if create_env_passes:
        # logging.debug("Build of env {} passed".format(tfile))
    # else:
        # logging.debug("Build of {} environment failed".format(tfile))
        # #If any builds fail the whole thing should fail
        # build_passes = False

    # status_checks_build(build_passes)

# def loop_files_upload(tfile):
    # """ Make sure the env uploads correctly """

    # upload_env_passes = True

    # if upload_remote_env(tfile):
        # logging.debug("Upload of environment {} passed".format(tfile))
    # else:
        # logging.warn("Upload of environment {} failed".format(tfile))
        # #If any uploads fail the whole thing should fail
        # upload_env_passes = False

    # status_checks_upload(upload_env_passes)
