# setup.py

# in case native support for PEP 660 is not available
from setuptools import setup, find_packages

setup(
    name='visualgo',
    version='2024.5.13',
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)
