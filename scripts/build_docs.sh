#!/usr/bin/env bash

set -ex

if [[ -z "${GITHUB_TOKEN}" ]] ; then
    echo "GitHub API key needs to be set to update docs."
    exit 0
fi

# Build the documentation
#GITHUB_USERNAME=${TRAVIS_REPO_SLUG%/*}

cd /nyuad-conda-configs

#At least we can test if this works
mkdir -p _docs

echo "BUILDING DOCS"

git status
git add -A

git config  user.email "nobody@nobody.org"
git config  user.name "Travis CI"

ORIGIN="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
git remote rm origin
git remote add origin "$ORIGIN"
git checkout "$TRAVIS_BRANCH"

git add _docs
#IF it doesn't exit as 0 its because there is nothing to commit
git commit  -m "Updated docs to commit ${TRAVIS_COMMIT}." || exit 0
git push -f "$ORIGIN" "$TRAVIS_BRANCH"
