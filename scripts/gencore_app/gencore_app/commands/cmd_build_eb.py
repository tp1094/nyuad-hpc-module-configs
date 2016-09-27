import click
import os
from jinja2 import Environment, FileSystemLoader

from gencore_app.cli import global_test_options
from gencore_app.utils.main import find_files, from_file, get_name, remote_env_exists

@click.command('build_eb', short_help='Build Easyblock Configs')
@global_test_options
def cli(verbose, environments):
    """Build  Easyblock Configs."""

    click.echo("Building Easyblock Configs")

    cwd = os.getcwd()

    click.echo("We are in dir {}".format(cwd))

    files = find_files(environments)

    if not os.path.exists('_easybuild'):
        os.makedirs('_easybuild')

    for filename in files:
        env = from_file(filename)

        ##TODO Make this a method of main
        ##This should be a method
        force_rebuild = False
        if 'rebuild' in env.extra_args and env.extra_args['rebuild'] is not True:
            force_rebuild = True

        if force_rebuild or not remote_env_exists(filename):
            click.echo("We are creating eb for {}".format(filename))
            name, version = get_name(filename)
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
