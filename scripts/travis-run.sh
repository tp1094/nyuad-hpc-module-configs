#!/bin/bash

set -euo pipefail

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    git checkout $TRAVIS_BRANCH
    git pull origin $TRAVIS_BRANCH

    #Use docker container to run tests
    docker run -e TRAVIS_PULL_REQUEST -e TRAVIS_BRANCH -e ANACONDA_TOKEN -e ANACONDA_PASSWORD -e ANACONDA_USER  -i -t -v `pwd`:/nyuad-conda-configs jerowe/nyuad-anaconda /nyuad-conda-configs/scripts/run-tests.sh

else
    exit 0
fi
