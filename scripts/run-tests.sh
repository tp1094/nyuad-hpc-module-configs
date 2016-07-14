#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs

### Begin Run Tests

echo "This is a TEST!" >> test.md

### End Run Tests
