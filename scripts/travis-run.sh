#!/bin/bash

set -euo pipefail

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    git checkout $TRAVIS_BRANCH
    git pull origin $TRAVIS_BRANCH

    #Use docker container to run tests

    if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = true ]]
    then
        echo "On master branch..."
        echo "Doing nothing first time darnit"
        #python3 scripts/test_environments.py --master
    else
        echo "Not on master branch..."
        #python3 scripts/test_environments.py
        docker run -e TRAVIS_PULL_REQUEST -e TRAVIS_BRANCH -e ANACONDA_TOKEN -e ANACONDA_PASSWORD -e ANACONDA_USER  -i -t -v `pwd`:/nyuad-conda-configs jerowe/nyuad-anaconda /nyuad-conda-configs/scripts/run-tests.sh
    fi

else
    exit 0
fi
