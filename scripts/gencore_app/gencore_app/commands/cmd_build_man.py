import click
from gencore_app.cli import global_test_options
from conda_env import env
from gencore_app.utils.main import find_files, run_command
import logging
import os
import sys
import yaml

logging.basicConfig(level=logging.DEBUG)

@click.command('build_man', short_help='Build man')
@global_test_options
def cli(verbose, environments, force_rebuild):
    """Build man pages."""

    click.echo("hello")

    files = find_files(environments)

    for tfile in files:
        get_name(tfile)

def get_name(fname):

    package = env.from_file(fname)
    name  = package.name
    marked = '_docs/environment/{}.md'.format(name)

    l = name.split("_")
    version = l.pop()
    name = "_".join(l)

    click.echo("")
    docs = DocPackage(name + "_docs", version, marked, fname)

    click.echo("Name is " + docs.name)

    make_man(docs)

def make_man(docs):

    cwd = os.getcwd()

    man_dir = "build/{}/man/man1".format(docs.name)

    if not os.path.exists(man_dir):
        os.makedirs(man_dir)

    cmd = "marked-man {} > {}/{}.1.man".format(docs.marked, man_dir, docs.name)

    man_passes = run_command(cmd)

    status_check_man(man_passes)

    os.chdir(man_dir)
    cmd = "gzip {}.1.man".format(docs.name)

    man_passes = run_command(cmd)
    status_check_man(man_passes)
    os.chdir(cwd)

    make_doc_package(docs)

def make_doc_package(docs):

    cwd = os.getcwd()
    recipe_dir = "build/" + docs.name + "/conda.recipe"

    if not os.path.exists(recipe_dir):
        os.makedirs(recipe_dir)

    os.chdir(recipe_dir)

    d = {'package': {'name': docs.name, 'version': docs.version}, 'source': {'path': '{}/build/{}'.format(cwd, docs.name)} }

    with open('meta.yaml', 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)

    yaml.dump(d)
    logging.debug("We made the yaml files")

    os.chdir(cwd)

def update_env(docs):

    env_data = env.from_file(docs.env_file)

    env_data.dependencies.add("{}_docs={}".format(docs.name, docs.version))

    env_data.save()

def status_check_man(man_passes):

    if not man_passes:
        logging.warn("One or more man pages did not pass!")
        sys.exit(1)

class DocPackage(object):

    def __init__(self, name, version, marked, env_file):
        self.name = name
        self.version = version
        self.marked = marked
        self.env_file = env_file
