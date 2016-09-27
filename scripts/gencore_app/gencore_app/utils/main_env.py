from conda_env.env import Environment
from conda_env.env import Dependencies
from conda_env import exceptions, compat
import logging
import yaml
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Environment(Environment):
    def __init__(self, name=None, filename=None, channels=None,
                 dependencies=None, prefix=None, **kwargs):
        self.name = name
        self.filename = filename
        self.prefix = prefix
        self.dependencies = Dependencies(dependencies)

        if channels is None:
            channels = []
        self.channels = channels
        self.extra_args = kwargs

    def to_dict_extra_args(self):
        d = yaml.dict([('name', self.name)])
        if self.channels:
            d['channels'] = self.channels
        if self.dependencies:
            d['dependencies'] = self.dependencies.raw
        if self.prefix:
            d['prefix'] = self.prefix
        if self.extra_args:
            d['extra_args'] = self.extra_args
        return d

    def to_yaml_extra_args(self, stream=None):
        d = self.to_dict_extra_args()
        out = compat.u(yaml.dump(d, default_flow_style=False))
        if stream is None:
            return out
        stream.write(compat.b(out, encoding="utf-8"))

    def save_extra_args(self):
        with open(self.filename, "wb") as fp:
            self.to_yaml_extra_args(stream=fp)

def from_yaml(yamlstr, **kwargs):
    """Load and return a ``Environment`` from a given ``yaml string``"""
    data = yaml.load(yamlstr)
    if kwargs is not None:
        for key, value in kwargs.items():
            data[key] = value
    return Environment(**data)

def from_file(filename):
    if not os.path.exists(filename):
        raise exceptions.EnvironmenfilenameNotFound(filename)
    with open(filename, 'r') as fp:
        yamlstr = fp.read()
        return from_yaml(yamlstr, filename=filename)
