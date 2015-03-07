#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    rack-ddnsm
    ~~~~~

    Dynamic DNS metadata for Rackspace Cloud DNS, 
    manages TXT records containing metadata in the format of title,desc,data.

    :copyright: (c) 2015 by Alex Edwards.
    :license: MIT, see LICENSE for more details.

    :repo: <https://github.com/sunshinekitty/rack-ddnsm>
    :docs: <https://github.com/sunshinekitty/rack-ddnsm/wiki>
    
"""

from setuptools import setup
import re

with open("rack-ddnsm/version.py", "rt") as vfile:
    version_text = vfile.read()
vmatch = re.search(r'version ?= ?"(.+)"$', version_text)
version = vmatch.groups()[0]

setup(
    name="rack-ddnsm",
    version=version,
    description="Python language bindings for Encore.",
    author="Alex Edwards",
    author_email="edwards@linux.com",
    url="https://github.com/sunshinekitty/rack-ddnsm>",
    keywords="rackspace cloud dns meta ddns dns",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
    ],
    install_requires=[
        "requests>=2.2.1",
        "dnspython>=1.12.0"
    ],
    packages=[
        "rack-ddnsm",
    ]
)
