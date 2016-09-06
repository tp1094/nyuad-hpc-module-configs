#gencore_app.commands.cmd_build_envs

import click
from gencore_app.cli import global_test_options
from gencore_app.utils.main import find_files, remote_env_exists
from gencore_app.utils.main_build_env import status_check_build, try_conda_env_create

@click.command('build_envs', short_help='Build environments')
@global_test_options

def cli(verbose, environments, force_rebuild):
    """1. Check remote env exists.
       2. Build the env.
       3. Exit if anything bad happens """

    click.echo("environments are {}".format(environments))

    files = find_files(environments)
    click.echo('files are {}'.format(files))

    for tfile in files:
        env_exists = remote_env_exists(tfile)
        click.echo("Does the env exist? {}".format(env_exists))

        if force_rebuild or not env_exists:
            build_passes = try_conda_env_create(tfile)
            status_check_build(build_passes)
        else:
            click.echo("env exists we are skipping")
