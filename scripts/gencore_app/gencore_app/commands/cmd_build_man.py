import click
from gencore_app.cli import global_test_options
from conda_env import env
from gencore_app.utils.main import find_files, run_command
import logging
import os
import sys
import yaml
import shutil
from binstar_client.utils import get_server_api

logging.basicConfig(level=logging.DEBUG)

aserver_api = get_server_api()

@click.command('build_man', short_help='Build man')
@global_test_options
def cli(verbose, environments, force_rebuild):
    """Build man pages."""

    click.echo("hello")

    files = find_files(environments)
    cwd = os.getcwd()

    for tfile in files:
        get_name(tfile)
        os.chdir(cwd)

def get_name(fname):

    package = env.from_file(fname)
    name  = package.name
    marked = '_docs/environment/{}.md'.format(name)

    l = name.split("_")
    version = l.pop()
    name = "_".join(l)

    click.echo("")
    docs = DocPackage(name , version, marked, fname)

    click.echo("Name is " + docs.name)

    make_man(docs)

def make_man(docs):

    man_dir = "build/{}/share/man/man1".format(docs.name)

    if not os.path.exists(man_dir):
        os.makedirs(man_dir)

    cmd = "marked-man {} > {}/{}.1".format(docs.marked, man_dir, docs.name)

    man_passes = run_command(cmd)

    status_check_man(man_passes)

    make_doc_package(docs)

def make_doc_package(docs):

    if remote_docs_exist(docs):
        return

    cwd = os.getcwd()
    recipe_dir = "build/" + docs.name + "/conda.recipe"

    build_template = cwd + "/package_template/build.sh"

    if not os.path.exists(recipe_dir):
        os.makedirs(recipe_dir)

    shutil.copyfile(build_template, recipe_dir + "/build.sh")

    os.chdir(recipe_dir)
    name = docs.name

    d = {'package': {'name': name + "_docs", 'version': docs.version}, 'source': {'path': '{}/build/{}'.format(cwd, docs.name)} }

    with open('meta.yaml', 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)

    yaml.dump(d)
    logging.debug("We made the yaml files")

    cmd = "conda build ./"
    status = run_command(cmd, True)
    status_check_man(status)

    os.chdir(cwd)

    update_env(docs)

def update_env(docs):

    env_data = env.from_file(docs.env_file)

    env_data.dependencies.add("{}_docs={}".format(docs.name, docs.version))

    env_data.save()

def remote_docs_exist(docs):

    name  = docs.name
    version = docs.version
    logging.debug("Testing for docs package name {}".format(name))

    try:
        aserver_api.release(os.environ.get("ANACONDA_USER"), name, version)
        logging.debug("Remote doc package exists. Next!")
    except:
        logging.debug("Remote doc package does not exist. Build")
        return False

    return True

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
