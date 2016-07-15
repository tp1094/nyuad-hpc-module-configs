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

        if output:
            logging.debug(output)

        ec = p.poll()
        logging.debug("Exit Code {}".format(ec))

    # read remaining data (all of it)
    output = p.stdout.read(readSize).decode("utf-8")

    if output:
        logging.debug(output)

    if ec == 0:
        return True
    else:
        return False

def try_remote_env_exists(fname):

    package = env.from_file(fname)
    logging.debug("Testing for package name {}".format(package.name))

    #Add --force just in case prefix already exists exists
    cmd = "anaconda show " + os.environ.get("ANACONDA_USER") + "/" + package.name
    return run_command(cmd)

#Move this to only upload on master

def upload_remote_env(fname):

    logging.debug("Uploading remote env of {}".format(fname))
    cmd = "conda env upload -f {}".format(fname)
    return run_command(cmd)

def try_conda_env_create(fname):

    retries_max = 1
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

def loop_files(files):

    build_passes = True
    upload_env_passes = True

    create_env = False

    for tfile in files:

        logging.debug("Trying file {}".format(tfile))

        if try_remote_env_exists(tfile):
            logging.debug("Remote env exists. Next!")
            create_env = True
            continue
        else:
            logging.debug("Remote env does not exist! Don't skip!")
            create_env = try_conda_env_create(tfile)

        if not create_env:
            logging.debug("Build of {} environment failed".format(tfile))
            build_passes = False
        else:
            logging.debug("Build of env {} passed".format(tfile))

            if args.master:
                if upload_remote_env(tfile):
                    logging.debug("Upload of environment {} passed".format(tfile))
                else:
                    logging.warn("Upload of environment {} failed".format(tfile))
                    upload_env_passes = False

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

def find_files():

    files = glob.glob("**/test/environment*.yml", recursive=True)

    return files

##MAIN

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="Build and upload conda env environments")
    p.add_argument("--environments",
                   nargs="+",
                   help="List of environmental files to build")
    p.add_argument("--master",
                   help="Build master branch",
                   default=False,
                   action="store_true")

    global args
    args = p.parse_args()

    if args.environments:
        files = args.environments
    else:
        files = find_files()

    # if os.environ.get("TRAVIS_BRANCH") is 'master':
        # args.master = True

    loop_files(files)
