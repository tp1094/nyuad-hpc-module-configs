#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs
#conda config --add channels https://conda.anaconda.org/t/$ANACONDA_TOKEN/$ANACONDA_USER

anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

### Begin Run Tests

#python3 scripts/md5-check.py
python3 scripts/test_environments.py

### End Run Tests
