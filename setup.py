"""
setup
~~~~~

A script for creating Python packages.
"""
__version__ = '0.1.0'


import importlib
import os
import setuptools


def get_package_name() -> str:
    """Get the name of the package."""
    cwd = os.getcwd()
    return cwd.split(os.path.sep)[-1]


pkg_name = get_package_name()
pkg_metadata = importlib.import_module(f'{package_name}.__version__')
with open('requirements.txt') as fh:
    reqs = fh.readlines()
    reqs = [req for req in reqs if not req.startswith('-')]
with open('README.rst') as fh:
    long_desc = fh.read()

setuptools.setup(
    name=pkg_name,
    version=pkg_metadata.__version__,
    description=pkg_metadata.__description__,
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    url=f'https://github.com/pji/{package_name}',
    author=pkg_metadata.__author__,
    install_requires=reqs,
    author_email='pji@mac.com',
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
    zip_safe=False
)
