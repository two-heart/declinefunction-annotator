#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeQL for Python.
"""

import os
import settings
import subprocess
import tempfile
from typing import Iterable
import uuid

# Configuration
codeql_path = 'codeql'
search_path = None
library_path = None

# Temporaries
temp_path = None


def temporary_root():
    global temp_path
    if temp_path is None:
        temp_path = tempfile.TemporaryDirectory(prefix="codeql-python_")
    return temp_path.name


def temporary_path(prefix, suffix):
    name = ''
    if prefix:
        name += prefix
    name += uuid.uuid4().hex
    if suffix:
        name += suffix
    return os.path.join(temporary_root(), name)


def temporary_dir(create=True, prefix=None, suffix=None):
    path = temporary_path(prefix, suffix)
    if create:
        os.mkdir(path)
    return path


def temporary_file(create=True, prefix=None, suffix=None):
    path = temporary_path(prefix, suffix)
    if create:
        open(path, 'a').close()
    return path


def temporary_query_file() -> str:
    location = settings.query_home
    # create a file that does not yet exist in location
    return tempfile.NamedTemporaryFile(dir=location, delete=False).name


# Environment
def set_search_path(path):
    global search_path
    if isinstance(path, Iterable):
        separator = ';' if os.name == 'nt' else ':'
        path = separator.join(path)
    search_path = path


def run(args):
    command = [codeql_path] + list(map(str, args))
    return subprocess.run(command, stdout=subprocess.DEVNULL)
