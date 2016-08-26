#!/usr/bin/env python3

import subprocess as sp
import os
import sys
import logging
from conda_env import env
import glob
import argparse

logging.basicConfig(level=logging.DEBUG)

def run_command(cmd):

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

        if output and args.verbose:
            logging.debug(output)

        ec = p.poll()

    # read remaining data (all of it)
    output = p.stdout.read(readSize).decode("utf-8")

    if output and args.verbose:
        logging.debug(output)

    logging.debug("Exit Code {}".format(ec))

    if ec == 0:
        return True
    else:
        return False

def try_remote_env_exists(fname):

    package = env.from_file(fname)
    logging.debug("Testing for package name {}".format(package.name))

    cmd = "anaconda show " + os.environ.get("ANACONDA_USER") + "/" + package.name
    return run_command(cmd)

def upload_remote_env(fname):

    logging.debug("Uploading remote env of {}".format(fname))
    cmd = "conda env upload -f {}".format(fname)
    return run_command(cmd)

def try_conda_env_create(fname):

    retries_max = 2
    retries_count = 0
    create_env = False

    while retries_count <= retries_max:
        retries_count = retries_count + 1
        ec = run_conda_env_create(fname)
        if ec:
            logging.info('Conda Env for {} created successfully'.format(fname) )
            create_env = True
            break
        else:
            logging.warn('Conda Env was NOT created successfully! Retrying {}'.format(retries_count))

    return create_env

def run_conda_env_create(fname):

    logging.debug("Testing environment build file {}".format(fname))
    cmd = "conda env create --force --file {}".format(fname)
    return run_command(cmd)

def status_checks(build_passes, upload_env_passes):

    if not build_passes:
        logging.warn("One or more builds did not pass!")
        sys.exit(1)
    else:
        logging.info("All builds passed!")
        sys.exit(0)

    if args.master:
        if not upload_env_passes:
            logging.warn("One or more uploads failed!")
            sys.exit(1)
        else:
            logging.info("All uploads passed!")
            sys.exit(0)

def loop_files(files):

    build_passes = True
    upload_env_passes = True
    create_env_passes = None

    for tfile in files:

        logging.debug("Trying file {}".format(tfile))

        if try_remote_env_exists(tfile):
            logging.debug("Remote env exists. Next!")
            continue
        else:
            logging.debug("Remote env does not exist! Don't skip!")
            create_env_passes = try_conda_env_create(tfile)

        if create_env_passes:
            logging.debug("Build of env {} passed".format(tfile))
        else:
            logging.debug("Build of {} environment failed".format(tfile))
            #If any builds fail the whole thing should fail
            build_passes = False

        if args.master and create_env_passes:
            if upload_remote_env(tfile):
                logging.debug("Upload of environment {} passed".format(tfile))
            else:
                logging.warn("Upload of environment {} failed".format(tfile))
                #If any uploads fail the whole thing should fail
                upload_env_passes = False

    status_checks(build_passes, upload_env_passes)

def find_files():

    if args.environments:
        return  args.environments
    else:
        return  glob.glob("**/environment*.yml", recursive=True)

##MAIN
#TODO add in separate workflow for updating

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="Build and upload conda env environments")
    p.add_argument("--environments",
                   nargs="+",
                   help="List of environmental files to build")
    p.add_argument("--master",
                   help="Build master branch",
                   default=False,
                   action="store_true")
    p.add_argument("--verbose",
                   help="print stdout of commands",
                   default=False,
                   action="store_true")

    global args
    args = p.parse_args()

    files = find_files()
    loop_files(files)
