#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH

conda install -y pip

cd /nyuad-conda-configs

cd scripts/gencore_app
python setup.py build && python setup.py install

cd /nyuad-conda-configs

if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    #Upload packages
    #TODO One script for testing and one for uploading

    anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD

    echo "Uploading packages to anaconda!"
    gencore_app upload_envs --force_rebuild --environment recipes/variant_detection/1.0/environment-1.0.yml

else
    #Just test packages
    gencore_app build_envs --force_rebuild --environment recipes/variant_detection/1.0/environment-1.0.yml
    gencore_app upload_envs --force_rebuild --environment recipes/variant_detection/1.0/environment-1.0.yml
fi
