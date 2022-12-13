#!/usr/bin/env python
from os.path import abspath
from os.path import dirname
from os.path import join
from setuptools import setup
from setuptools import find_packages

cwd = abspath(dirname(__file__))

with open(join(cwd, 'README.md'), 'r') as readme_file:
    long_description = readme_file.read()

with open(join(cwd, 'requirements.txt')) as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='atlas',
    version='1.0',
    author='Kendrick Horeftis',
    author_email='kendrick@horeft.is',
    description=(
        'Data Engineering Challenge'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/khoreftis/data-engineering',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=requirements,
    entry_points='''
    [console_scripts]
    atlas=atlas.main:main
    ''',
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    platforms='any',
    include_package_data=True,
)