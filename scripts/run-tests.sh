#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

yum install -y git
export PATH=/anaconda/bin:$PATH
python --version

cd /nyuad-conda-configs

REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

git checkout $TRAVIS_BRANCH

git config user.name "Jillian Rowe"
git config user.email "jillian.e.rowe@gmail.com"

### Begin Run Tests

echo "This is a TEST!" >> test.md

### End Run Tests
