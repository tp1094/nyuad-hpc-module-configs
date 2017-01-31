#!/bin/bash
set -e

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    docker pull quay.io/nyuad_cgsb/anaconda-centos
else

    exit 0
fi
