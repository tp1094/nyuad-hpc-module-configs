#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH

cd /nyuad-conda-configs

anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    #Upload packages
    #TODO One script for testing and one for uploading
    echo "Uploading packages to anaconda!"
    python3 tests/test_environments.py --master
    python3 scripts/build_docs.py --master
    scripts/build_docs.sh
else
    #Just test packages
    python3 tests/test_environments.py
fi
