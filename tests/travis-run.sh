#!/bin/bash

set -euo pipefail

if [[ $TRAVIS_OS_NAME = "linux" ]]
then

    docker run -e TRAVIS_PULL_REQUEST -e TRAVIS_BRANCH \
        -e GITHUB_TOKEN -e GITHUB_USER -e GITHUB_REPO \
        -e ANACONDA_TOKEN -e ANACONDA_PASSWORD -e ANACONDA_USER \
        -i -t -v `pwd`:/nyuad-conda-configs quay.io/nyuad_cgsb/anaconda-centos /nyuad-conda-configs/tests/run-tests.sh

else
    exit 0
fi
