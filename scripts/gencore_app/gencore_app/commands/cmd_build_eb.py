import click
from gencore_app.cli import global_test_options
from gencore_app.utils.main import find_files, get_name
import logging
from binstar_client.utils import get_server_api

from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.DEBUG)

aserver_api = get_server_api()

@click.command('build_eb', short_help='Build Easyblock Configs')
@global_test_options
def cli(verbose, environments, force_rebuild):
    """Build  Easyblock Configs."""

    click.echo("Building Easyblock Configs")

    files = find_files(environments)

    for tfile in files:
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
