import click
import os
from jinja2 import Environment, FileSystemLoader

from gencore_app.cli import global_test_options
from gencore_app.utils.main import find_files, get_name, remote_env_exists

@click.command('build_eb', short_help='Build Easyblock Configs')
@global_test_options
def cli(verbose, environments, force_rebuild):
    """Build  Easyblock Configs."""

    click.echo("Building Easyblock Configs")

    cwd = os.getcwd()

    click.echo("We are in dir {}".format(cwd))

    files = find_files(environments)

    if not os.path.exists('_easybuild'):
        os.makedirs('_easybuild')

    for tfile in files:
        if force_rebuild or not remote_env_exists(tfile):
            name, version = get_name(tfile)
            print_html_doc(name, version)

def print_html_doc(name, version):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader('package_template'),
                         trim_blocks=False)
    tmp = j2_env.get_template('template.eb').render(name=name, version=version)

    f = open('_easybuild/{}-{}.eb'.format(name, version), 'w')
    f.write(tmp)
    f.close()
