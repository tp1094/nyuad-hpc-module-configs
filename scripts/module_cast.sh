#!/usr/bin/env bash

# Verbose and exit on errors
set -x -e

#########################################################
# This script installs anaconda, configures the conda environment, and creates
# a single software stack - gencore_variant_detection_1.0

# It will take some time to run the first time. Subsequent times, packages will
# be cached, and the time to create a software stack will decrease.
#########################################################

#########################################################
# 1. Install Anaconda
#########################################################

ANACONDA_URL="https://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh"
ANACONDA_SCRIPT="Anaconda3-4.0.0-Linux-x86_64.sh"

# Path to executables and libraries
INSTALL_SITE="${HOME}/.local/anaconda3"

wget $ANACONDA_URL

chmod 777 $ANACONDA_SCRIPT &&  "./${ANACONDA_SCRIPT}" -p $INSTALL_SITE -b -f

#Add this to your bashrc
export PATH="${INSTALL_SITE}/bin:${PATH}"

#Make sure anaconda installs properly
which conda

#########################################################
# 2. Configure Anaconda Environment
#########################################################

#Add default packages
conda config --add create_default_packages setuptools
conda config --add create_default_packages ipython

#Add default channels
conda config --add channels bioconda
conda config --add channels r

#Install conda env
conda install conda-env

#########################################################
# 3. Install Software Stacks
#########################################################

#Create the software stack
conda env create --quiet jerowe/gencore_variant_detection_1.0

#Use the software stack
source activate gencore_variant_detection_1.0

#Try it out!
which perl
which R
which trimmomatic
which picard
