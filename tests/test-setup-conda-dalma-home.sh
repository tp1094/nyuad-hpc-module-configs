#!/usr/bin/env bats

function start_tests() {
	echo "Remove existing conda envs"
	rm -rf "$HOME/.conda"
	rm -rf "$HOME/.condarc"

    #HPC specific
	rm -rf "/home/$USER/.conda"
}

function end_tests() {
	echo "this is the teardown"

	rm -rf $HOME/.conda
	rm -rf $HOME/.condarc

    #HPC specific
	rm -rf "/home/$USER/.conda"
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
	run sh -c "mkdir -p /home/$USER/.conda"
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

