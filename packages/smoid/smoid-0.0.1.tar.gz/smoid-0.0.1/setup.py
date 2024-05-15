import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'smoid'
AUTHOR = 'Cesar'
AUTHOR_EMAIL = 'unit@noreply.com'
LICENSE = 'MIT License'
DESCRIPTION = 'smoid is a package that allows you to monitor signals from a machine and send them to a server.'
# Read the contents of your README file for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Add your required packages to INSTALL_REQUIRES list
INSTALL_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',  # Specify the type of content
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)