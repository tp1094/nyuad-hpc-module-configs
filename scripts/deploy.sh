#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

#if [ -z $TARGET_BRANCH ]; then
	##We're not in travis
	#echo "No changes to the spec on this push; exiting."
	#exit 0
#fi

#yum install -y git
#export PATH=/anaconda/bin:$PATH

#cd /nyuad-conda-configs

echo "We are in deploy.sh"

REPO=`git config remote.origin.url`
SSH_REPO=${REPO/https:\/\/github.com\//git@github.com:}
SHA=`git rev-parse --verify HEAD`

#git checkout $TRAVIS_BRANCH

#git config user.name "Jillian Rowe"
#git config user.email "jillian.e.rowe@gmail.com"

#### Begin Run Tests

#echo "This is a TEST!" >> test.md

#### End Run Tests

git add -A
git commit -m "Deploy MD5 sum checks: ${SHA}"

## Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
#export ENCRYPTION_LABEL="33e9f3ccc52a"
#export COMMIT_AUTHOR_EMAIL="jillian.e.rowe@gmail.com"
#export ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
#export ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
#export ENCRYPTED_KEY="${!ENCRYPTED_KEY_VAR}"
#export ENCRYPTED_IV="${!ENCRYPTED_IV_VAR}"

#openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in nyuad-hpc-module-configs-deploy.enc -out nyuad-hpc-module-configs-deploy -d
#openssl aes-256-cbc -K $encrypted_33e9f3ccc52a_key -iv $encrypted_33e9f3ccc52a_iv -in nyuad-hpc-module-configs-deploy.enc -out nyuad-hpc-module-configs-deploy -d
#openssl aes-256-cbc -K "33e9f3ccc52a" -in nyuad-hpc-module-configs-deploy.enc -out nyuad-hpc-module-configs-deploy -d

ls -lah
chmod 600 nyuad-hpc-module-configs-deploy
eval `ssh-agent -s`
ssh-add nyuad-hpc-module-configs-deploy

# Now that we're all set up, we can push.
git push $SSH_REPO $TRAVIS_BRANCH
