#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

echo "We are in deploy.sh"

if [ -z `git diff --exit-code` ]; then
    echo "No changes to the spec on this push; exiting."
    exit 0
fi

REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

git config user.name "Jillian Rowe"
git config user.email "jillian.e.rowe@gmail.com"

#git add -A
#git commit -m "Deploy MD5 sum checks: ${SHA}"

#ls -lah
#chmod 600 nyuad-hpc-module-configs-deploy
#eval `ssh-agent -s`
#ssh-add nyuad-hpc-module-configs-deploy

#git push $SSH_REPO $TRAVIS_BRANCH
