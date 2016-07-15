#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs

### Begin Run Tests

python3 scripts/md5-check.py

### End Run Tests
