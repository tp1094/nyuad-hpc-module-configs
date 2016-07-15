#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs

anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

### Begin Run Tests

python3 scripts/test_environments.py
if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    echo "On master branch..."
    python3 scripts/test_environments.py --master
else:
    echo "Not on master branch..."
    python3 scripts/test_environments.py
fi

### End Run Tests
