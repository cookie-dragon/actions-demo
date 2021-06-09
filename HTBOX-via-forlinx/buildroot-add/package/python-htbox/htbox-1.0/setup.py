from setuptools import setup, find_packages

import sys

install_requires = ["IPy"]

setup(name='htbox',
      version='1.0',
      description='Script for HTBOX',
      author='Cooky Long',
      author_email='lj12875@mail.haitian.com',
      packages=find_packages(),
      provides=["htbox"],
      install_requires=install_requires,
      include_package_data=True
      )
