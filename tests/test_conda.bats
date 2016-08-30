#!/usr/bin/env bats

function start_tests() {
	echo "Remove existing conda envs"
	rm -rf "$HOME/.conda"
	rm -rf "$HOME/.condarc"

    #HPC specific
	rm -rf "/scratch/$USER/.conda"
	rm -rf "/scratch/$USER/software/conda_create"
	rm -rf "/scratch/$USER/software/conda_env_create"
	rm -rf "/scratch/$USER/software/conda_create_perl"
	rm -rf "/scratch/$USER/software/conda_create_r"
}

function end_tests() {
	echo "this is the teardown"

	rm -rf $HOME/.conda
	rm -rf scratch/$USER/.conda
	rm -rf $HOME/.condarc

    #HPC specific
	rm -rf "/scratch/$USER/.conda"
	rm -rf "/scratch/$USER/software/conda_create"
	rm -rf "/scratch/$USER/software/conda_env_create"
	rm -rf "/scratch/$USER/software/conda_create_perl"
	rm -rf "/scratch/$USER/software/conda_create_r"
}

function conda_clean_all() {
	module purge && module load anaconda/2-4.1.1
	conda clean --all
}

@test "modules" {
    #To keep a cache of this packages don't remove the directories each time
    #To keep package cache - network problems - uncomment skip
    #skip
	start_tests
	run sh -c 'module purge && module load anaconda/2-4.1.1'
	[ "$status" = 0 ]
}

@test "make dirs" {
	run sh -c "mkdir -p /scratch/$USER/.conda"
	[ "$status" = 0 ]
}

@test "symbolic links" {
    #To keep a cache of this packages don't remove the directories each time
    #To keep package cache - network problems - uncomment skip
    #skip
	run sh -c "ln -s /scratch/$USER/.conda $HOME/.conda"
	[ "$status" = 0 ]
}

@test "conda config channels" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --add channels bioconda --add channels r"
	[ "$status" = 0 ]
}

@test "conda config default packages" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --add create_default_packages setuptools"
	[ "$status" = 0 ]
}

@test "conda config allow_softlinks" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --set allow_softlinks False"
	[ "$status" = 0 ]
}

@test "conda config always_copy" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --set always_copy True"
	[ "$status" = 0 ]
}

@test "conda config always_yes" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --set always_yes True"
	[ "$status" = 0 ]
}

@test "conda config env dirs" {
	run sh -c "module load anaconda/2-4.1.1 && conda config --add envs_dirs /home/$USER/.conda/envs"
	[ "$status" = 0 ]
}

#Create base env

@test "conda create" {
	echo "Creating base env"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /scratch/$USER/software/conda_create"
	[ "$status" = 0 ]
}

@test "conda create source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /scratch/$USER/software/conda_create"
	[ "$status" = 0 ]
}

@test "conda env create" {
	run sh -c "module load anaconda/2-4.1.1 && conda env create jerowe/gencore_python_1.0 -p /scratch/$USER/software/conda_env_create"
	[ "$status" = 0 ]
}

#Create perl env

@test "conda create perl" {
	echo "Creating perl env"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /scratch/$USER/software/conda_create_perl perl-app-cpaminus perl-termreadkey perl-dbi"
	[ "$status" = 0 ]
}

@test "conda create perl source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /scratch/$USER/software/conda_create_perl"
	[ "$status" = 0 ]
}

#Create r env

@test "conda create r" {
	echo "Creating r env"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /scratch/$USER/software/conda_create_r r r-base r-essentials"
	[ "$status" = 0 ]
}

@test "conda create r source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /scratch/$USER/software/conda_create_r"
	[ "$status" = 0 ]
}

