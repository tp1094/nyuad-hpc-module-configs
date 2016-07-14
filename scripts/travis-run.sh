#!/bin/bash

set -euo pipefail

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    docker run -e TRAVIS_BRANCH -e ENCRYPTION_LABEL -i -t -v `pwd`:/nyuad-conda-configs jerowe/nyuad-anaconda pwd
else

    exit 0
fi
