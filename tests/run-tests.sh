#!/bin/bash

set -e # Exit with nonzero exit code if anything fails

export PATH=/anaconda/bin:$PATH

conda install -y pip

cd /nyuad-conda-configs

cd scripts/gencore_app
python setup.py build && python setup.py install > /dev/null 2>&1

cd /nyuad-conda-configs

#gencore_app upload_envs --force_rebuild --environments recipes/variant_detection/1.0/environment-1.0.yml

if [[ $TRAVIS_BRANCH = "master" && "$TRAVIS_PULL_REQUEST" = false ]]
then
    #Upload packages
    anaconda login --user $ANACONDA_USER --password $ANACONDA_PASSWORD
    conda config --set anaconda_upload yes

    cd /nyuad-conda-configs

    gencore_app build_man --verbose --environments recipes/de_novo_genomic/1.0/environment-1.0.yml

    cd /nyuad-conda-configs
    gencore_app build_eb  --verbose --environments recipes/de_novo_genomic/1.0/environment-1.0.yml

    cd /nyuad-conda-configs
    scripts/build_easybuild.sh
    scripts/build_docs.sh

    echo "Uploading packages to anaconda!"
    gencore_app upload_envs --verbose --environments recipes/de_novo_genomic/1.0/environment-1.0.yml

    scripts/commit_recipes.sh
else
    #Just test packages
    #This is what it should be!
    gencore_app build_envs
fi
