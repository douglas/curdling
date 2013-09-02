from __future__ import absolute_import, unicode_literals, print_function
from pkg_resources import Requirement

import io
import os
import re
import tarfile


INCLUDE_PATTERN = re.compile(r'-r\s*\b([^\b]+)')

NAME_RE = re.compile(r'^([\w\_]+)')


def ext(fname):
    return os.path.splitext(fname)[1].split('#')[0]


def expand_requirements(file_name):
    requirements = []

    for req in io.open(file_name).read().splitlines():
        req = req.strip()
        if not req:
            break

        found = INCLUDE_PATTERN.findall(req)
        if found:
            requirements.extend(expand_requirements(found[0]))
        else:
            requirements.append(Requirement.parse(req))
    return requirements


def gen_package_path(package_name):
    path = list(package_name[:2])
    path.append(NAME_RE.findall(package_name)[0])
    return os.path.join(*path)