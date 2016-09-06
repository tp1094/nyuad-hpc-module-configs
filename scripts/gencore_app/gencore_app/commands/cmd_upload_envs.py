import click
from gencore_app.cli import global_test_options
from gencore_app.utils.main import find_files, remote_env_exists
from gencore_app.utils.main_upload import upload_remote_env, status_check_upload

@click.command('upload_envs', short_help='Upload environments to anaconda cloud')
@global_test_options
def cli(verbose, environments, force_rebuild):
    """ Only on master branch
        1. Check if remote env exists
        (Rebuild the env?)
        2. Upload the env to anaconda
    """

    click.echo("environments are {}".format(environments))

    files = find_files(environments)
    click.echo('files are {}'.format(files))

    for tfile in files:
        env_exists = remote_env_exists(tfile)
        click.echo("Does the env exist? {}".format(env_exists))

        if force_rebuild or not env_exists:
            upload_passes = upload_remote_env(tfile)
            status_check_upload(upload_passes)
        else:
            click.echo("env exists we are skipping")
