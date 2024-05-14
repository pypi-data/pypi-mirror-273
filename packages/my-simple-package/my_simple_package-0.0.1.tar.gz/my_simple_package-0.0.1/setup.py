from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name= 'my_simple_package', #name of the package which will be package dir below project
    version= '0.0.1',
    author='alon12345',
    author_email='alonf1536@gmail.com',
    description='simple test',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)