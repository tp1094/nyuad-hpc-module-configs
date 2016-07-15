#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs

anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

### Begin Run Tests

if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    python3 scripts/test_environments.py --master
else:
    python3 scripts/test_environments.py
fi

### End Run Tests
