#!/bin/bash

set -euo pipefail

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    docker run -e TRAVIS_BRANCH -e ENCRYPTION_LABEL -i -t -v `pwd`:/nyuad-conda-configs jerowe/nyuad-anaconda /nyuad-conda-configs/scripts/run-tests.sh
    ./scripts/deploy.sh
else
    exit 0
fi
