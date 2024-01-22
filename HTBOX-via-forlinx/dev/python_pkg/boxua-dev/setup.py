from setuptools import setup, find_packages

import sys

install_requires = ["asyncua", "ipaddress"]

setup(name='boxua',
      version='dev',
      description='OPCUA for HTBOX',
      author='Cooky Long',
      author_email='lj12875@mail.haitian.com',
      packages=find_packages(),
      provides=["boxua"],
      install_requires=install_requires,
      include_package_data=True
      )
