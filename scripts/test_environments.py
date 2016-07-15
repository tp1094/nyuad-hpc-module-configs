#!/usr/bin/env python3

import subprocess as sp
import os
import sys
import logging
from conda_env import env
import glob

logging.basicConfig(level=logging.DEBUG)


def try_remote_env_exists(fname):

    package_exists = True

    data = env.from_file(fname)
    package = data.name
    cmd = ["conda", "env", "create", "jerowe/" + package]

    try:
        sp.run(cmd, stdout=sp.PIPE, stderr=sp.STDOUT, check=True)
    except sp.CalledProcessError as e:
        print(e.stdout.decode(), file=sys.stderr)
        if b"does not exist" in e.stdout:
            logging.debug("Package {} does not exist".format(package))
            package_exists = False

    return package_exists


def upload_remote_env(fname):
    cmd = ["conda", "env", "upload", "-f", fname]

    env_upload = True
    try:
        sp.run(cmd, stdout=sp.PIPE, stderr=sp.STDOUT, check=True)
    except sp.CalledProcessError as e:
        # print(e.stdout.decode(), file=sys.stderr)
        logging.debug(e.stdout.decode())
        env_upload = False

    return env_upload

def find_files():

    create_env = False
    files = glob.glob("**/environment*.yml", recursive=True)

    for tfile in files:

        package_exists = try_remote_env_exists(tfile)

        if not package_exists:
            logging.debug("Package does not exist lets install")
            create_env = try_conda_create_env(tfile)

            write_build(create_env, tfile)


def try_conda_create_env(fname):

    retries_max = 3
    retries_count = 0
    create_env = False

    while retries_count <= retries_max:
        retries_count = retries_count + 1
        ec = run_conda_env_create(fname)
        if ec == 0:
            logging.info('Conda Env for {} created successfully'.format(fname) )
            create_env = True
            break
        else:
            logging.warn('Conda Env was NOT created successfully! Retrying {}'.format(retries_count))

    return create_env

def write_build(create_env, fname):

    if create_env:
        logging.debug("Build passed!")
    else:
        logging.debug("Build failed!")

def run_conda_env_create(fname):

    logging.debug("Testing file {}".format(fname))

    readSize = 1024 * 8
    cmd = "conda env create -f {}".format(fname)

    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE, close_fds=True, executable="/bin/bash")
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

    return ec

##MAIN

if __name__ == "__main__":

    find_files()
