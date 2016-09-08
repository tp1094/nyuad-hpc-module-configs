#!/usr/bin/env bash

set -ex

if [[ -z "${GITHUB_TOKEN}" ]] ; then
    echo "GitHub API key needs to be set to update docs."
    exit 0
fi

# Build the documentation
GITHUB_USERNAME=${TRAVIS_REPO_SLUG%/*}

cd /nyuad-conda-configs

#At least we can test if this works
mkdir -p _easybuild
git add _easybuild

git status

git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"

git commit --all -m "Updated docs to commit ${TRAVIS_COMMIT}."
git push -f -q "https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git" "$TRAVIS_BRANCH"
