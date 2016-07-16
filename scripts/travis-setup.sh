#!/bin/bash
set -e

if [[ $TRAVIS_OS_NAME = "linux" ]]
then
    docker pull jerowe/nyuad-anaconda
else

    exit 0
fi
