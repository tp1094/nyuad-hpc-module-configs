import subprocess as sp
import logging
import glob
from conda_env import env
from binstar_client.utils import get_server_api
import os

aserver_api = get_server_api()

logging.basicConfig(level=logging.DEBUG)

def run_command(cmd, verbose=False):

    logging.debug("Running cmd {}".format(cmd))
    readSize = 1024 * 8

    try:
        p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT,
                             stdin=sp.PIPE, close_fds=True, executable="/bin/bash")
    except OSError as err:
        print("OS Error: {0}".format(err))

    p.stdin.close()

    ec = p.poll()

    while ec is None:
        # need to read from time to time.
        # - otherwise the stdout/stderr buffer gets filled and it all stops working
        output = p.stdout.read(readSize).decode("utf-8")

        if output and verbose:
            logging.debug(output)

        ec = p.poll()

    # read remaining data (all of it)
    output = p.stdout.read(readSize).decode("utf-8")

    if output and verbose:
        logging.debug(output)

    logging.debug("Exit Code {}".format(ec))

    if ec == 0:
        return True
    else:
        return False

def find_files(environments):

    if environments:
        return  environments
    else:
        return  glob.glob("**/environment*.yml", recursive=True)

def get_name(fname):

    package = env.from_file(fname)
    name  = package.name

    l = name.split("_")
    version = l.pop()
    name = "_".join(l)

    return name, version

def remote_env_exists(tfile):

    #TODO Update this to use binstar utils
    env_config = env.from_file(tfile)
    logging.debug("Testing for package name {}".format(env_config.name))

    try:
        aserver_api.package(os.environ.get("ANACONDA_USER"), env_config.name)
        logging.debug("Remote env exists. Next!")
    except:
        logging.debug("Remote env does not exist! Don't skip!")
        return False

    return True
