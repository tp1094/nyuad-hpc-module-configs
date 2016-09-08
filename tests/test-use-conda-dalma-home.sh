#!/usr/bin/env bats

function start_tests() {

	rm -rf "/home/$USER/software/conda_create"
	rm -rf "/home/$USER/software/conda_create_perl"
	rm -rf "/home/$USER/software/conda_create_r"
}

function end_tests() {
	echo "this is the teardown"

	rm -rf "/home/$USER/software/conda_create"
	rm -rf "/home/$USER/software/conda_create_perl"
	rm -rf "/home/$USER/software/conda_create_r"
}

#Create base env

@test "conda create" {
	echo "Creating base env"
	run sh -c "rm -rf /home/$USER/software/conda_create"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /home/$USER/software/conda_create"
	[ "$status" = 0 ]
}

@test "conda create source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /home/$USER/software/conda_create"
	[ "$status" = 0 ]
}

#Create perl env

@test "conda create perl" {
	echo "Creating perl env"
	run sh -c "rm -rf /home/$USER/software/conda_create_perl"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /home/$USER/software/conda_create_perl perl-app-cpanminus perl-termreadkey perl-dbi"
	[ "$status" = 0 ]
}

@test "conda create perl source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /home/$USER/software/conda_create_perl"
	[ "$status" = 0 ]
}

#Create r env

@test "conda create r" {
	echo "Creating r env"
	run sh -c "rm -rf /home/$USER/software/conda_create_r"
	run sh -c "module load anaconda/2-4.1.1 && conda create -y -p /home/$USER/software/conda_create_r r r-base r-essentials"
	[ "$status" = 0 ]
}

@test "conda create r source activate" {
	run sh -c "module load anaconda/2-4.1.1 && source activate /home/$USER/software/conda_create_r"
	[ "$status" = 0 ]
}

