#!/bin/bash
set -e

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    docker pull nyuad_cgsb/anaconda-centos
else

    exit 0
fi
