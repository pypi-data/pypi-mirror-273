from setuptools import setup, find_packages
import os

# Get the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Use it to build the path to version.py
version_file = os.path.join(here, 'lib-version', 'version.py')

# Safely read the version from version.py
version = {}
with open(version_file, 'r') as file:
    exec(file.read(), version)

setup(
    name='lib_version_URLPhishing',
    version=version['__version__'],
    packages=find_packages(),
    description='A library to manage and track versions of software components'
)
