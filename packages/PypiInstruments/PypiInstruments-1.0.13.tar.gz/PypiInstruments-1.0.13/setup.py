from setuptools import setup
from setuptools import find_packages


setup(
    name="PypiInstruments",  # package name
    version="1.0.13",  # package version
    description='my package',  # package description
    packages=find_packages(),
    zip_safe=False,
)