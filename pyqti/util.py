#!/usr/bin/env python3

from importlib.resources import files
from string import Template

def read_resource(module, name):
    return files(module).joinpath(name).read_text(encoding="utf-8")

def load_template(name):
    return Template(read_resource('pyqti.templates', f"{name}.xml"))

