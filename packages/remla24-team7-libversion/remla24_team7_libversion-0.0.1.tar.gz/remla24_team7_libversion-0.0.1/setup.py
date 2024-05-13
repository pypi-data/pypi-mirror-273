from setuptools import find_packages, setup
from os.path import dirname, isdir, join
import os
import re
import subprocess


with open("README.md", "r") as f:
    long_description = f.read()


pwd = os.path.abspath(os.path.dirname(__file__))

version_file = os.path.join(pwd, 'versioning', 'version.py')

# Get current version
version = {}
with open(version_file, 'r') as file:
    exec(file.read(), version)

setup(
    name="remla24-team7-libversion",
    version=version['__version__'],
    url='https://github.com/remla24-team7/lib-version',
    author='Kevin Tran',
    description='A version-aware library that can can be asked for the version of the library.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['utility', 'versioning'],
    extras_require = {
        "dev": ["twine>=4.0.2", "bump2version==1.0.1"]
    }
)