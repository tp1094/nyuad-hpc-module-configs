#!/usr/bin/env python3

# import subprocess as sp
# import os
# import sys
from conda_env import env
import logging
import glob
import argparse
from binstar_client.utils import get_server_api

logging.basicConfig(level=logging.DEBUG)

class TrackSoftware():

    def __init__(self):
        self.deps = {}

class DepPackage():

    def __init__(self, name=None, version=None, summary=None, channel=None):
        self.name = name
        self.channel = channel
        self.version = version
        self.summary = summary
        self.envs = []

    def add_envs(self, env):
        self.envs.append(env)
        self.envs.sort()

class MeMyDocs():

    def __init__(self):
        self.track_software = TrackSoftware()
        self.files = []
        self.enviroment = None
        self.all_envs = []

    def add_envs(self):
        self.all_envs.append(self.environment)
        self.all_envs.sort()

    def parse_deps(self, dep):

        dep_split = dep.split('=')

        if len(dep_split) == 2:
            #There is a version
            package_name = dep_split[0]
            package_version = dep_split[1]
        else:
            #There is no version
            package_name = dep_split[0]
            package_version = 'latest'

        return package_name, package_version

    def search_deps(self, dep, version, channels):

        key = "{}={}".format(dep, version)

        if  key not in self.track_software.deps.keys():
            aserver_api = get_server_api()
            packages = aserver_api.search(dep)

            for package in packages:
                if package['owner'] in channels and package['name'] == dep:
                    dep_obj = DepPackage(dep, version, package['summary'], package['owner'] )
                    self.track_software.deps[key] = dep_obj
                    dep_obj.add_envs(self.environment)
                    return dep_obj

            #must come from default or channels not defined in environment.yml
            dep_obj = DepPackage(dep, version, '', 'default' )
            dep_obj.add_envs(self.environment)
            self.track_software.deps[key] = dep_obj
            return dep_obj
        else:
            dep_obj  = self.track_software.deps[key]

            if self.environment not in dep_obj.envs:
                dep_obj.add_envs(self.environment)

            return dep_obj

    def write_env_markdown(self, fname):

        package = env.from_file(fname)

        name  = package.name
        self.environment = name
        self.add_envs()

        p_dict = package.to_dict()
        deps = p_dict['dependencies']
        deps.sort()
        channels = p_dict['channels']

        # f = open('/nyuad-conda-configs/_docs/environment/{}.md'.format(name), 'w')
        f = open('_docs/environment/{}.md'.format(name), 'w')

        f.write("# {}\n".format(name))

        f.write("## Summary\n\n")

        f.write("Coming soon!")

        f.write("## Software Packages\n\n")

        for dep in deps:
            package_name, package_version = self.parse_deps(dep)

            package_obj = self.search_deps(package_name, package_version, channels)

            f.write("### {}\n".format(package_name))

            f.write("Version: {}\n".format(package_version))
            f.write("Conda Channel: {}\n".format(package_obj.channel))
            f.write("Summary: {}\n".format(package_obj.summary))
            f.write("\n")
            f.write("\n")

        f.close()

    def write_software_markdown(self):

        f = open('_docs/software/software.md', 'w')
        f.write("# Software\n\n")

        keys = self.track_software.deps.keys()
        dep_keys = list(keys)
        dep_keys.sort()

        for dep_name in dep_keys:
            dep_obj = self.track_software.deps[dep_name]

            f.write("### {}\n\n".format(dep_obj.name.capitalize()))
            f.write("#### Summary\n\n")
            f.write("{}\n\n".format(dep_obj.summary))
            f.write("**Version** {}\n".format(dep_obj.version))
            f.write("**Conda Channel** {}\n".format(dep_obj.channel))
            f.write("#### HPC Modules\n")

            #TODO Format these as urls
            for tenv in dep_obj.envs:
                f.write("\t* {}\n".format(tenv))

            f.write("\n")
            f.write("\n")

        f.close()

    def write_summary_markdown(self):

        f = open('_docs/SUMMARY.md', 'w')
        f.write("# Summary\n\n")

        f.write("* [Overview](overview.md)\n")
        f.write("* [Software](software/software.md)\n")
        f.write("* [HPC Modules](environment/environments.md)\n")

        for tenv in self.all_envs:
            f.write("\t* [{}](environment/{}.md)\n".format(tenv.capitalize(), tenv))

    def find_files(self):

        if args.environments:
            # return  args.environments
            self.files = args.environments
        else:
            # return  glob.glob("**/environment*.yml", recursive=True)
            self.files = glob.glob("**/environment*.yml", recursive=True)

        for fname in self.files:
            self.write_env_markdown(fname)

        self.write_software_markdown()
        self.write_summary_markdown()

if __name__ == "__main__":

    p = argparse.ArgumentParser(description="Build docs")
    p.add_argument("--environments",
                   nargs="+",
                   help="List of environmental files to build")
    p.add_argument("--master",
                   help="Build master branch",
                   default=False,
                   action="store_true")
    p.add_argument("--verbose",
                   help="print stdout of commands",
                   default=False,
                   action="store_true")

    global args
    args = p.parse_args()

    docs = MeMyDocs()

    docs.find_files()
