from setuptools import setup
from setuptools import find_packages


VERSION = '0.1.1'

setup(
    name='autowx_sdk',  # package name
    version=VERSION,  # package version
    description='my package',  # package description
    packages=find_packages(),
    zip_safe=False,
)