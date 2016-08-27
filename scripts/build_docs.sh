#!/bin/bash

set -ev

if [[ ! -z "${GITHUB_TOKEN}" ]] ; then
    echo "GitHub API key needs to be set to update docs."
    exit 0
fi

#cd "${TRAVIS_BUILD_DIR}/_docs"

# Build the documentation
GITHUB_USERNAME=${TRAVIS_REPO_SLUG%/*}

git add _docs
git config user.name "Travis CI"
git commit --all -m "Updated docs to commit ${TRAVIS_COMMIT}."
git push -f -q "https://${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/nyuad-hpc-module-configs.git" master &> /dev/null
