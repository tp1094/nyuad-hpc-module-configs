#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH

cd /nyuad-conda-configs

anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    #Upload packages
    echo "Uploading packages to anaconda!"
    python3 scripts/test_environments.py --master
else
    #Just test packages
    python3 scripts/test_environments.py
fi
