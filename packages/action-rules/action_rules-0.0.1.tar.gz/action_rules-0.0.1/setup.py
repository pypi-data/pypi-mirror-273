from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='action_rules',
    version='0.0.1',
    url='https://github.com/lukassykora/actionrules',
    author='Lukas Sykora',
    author_email='lukas.sykora@vse.cz',
    description='Action Rules Mining Tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas~=2.2.2'],
)
