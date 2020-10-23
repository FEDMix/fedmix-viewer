#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup
import codecs


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='fedmix_backend',
    version=get_version('fedmix_backend/__version__.py'),
    description="GraphQL backend for the fedmix frontend",
    long_description=readme + '\n\n',
    author="Berend Weel",
    author_email='b.weel@esciencecenter.nl',
    url='https://github.com/FEDMix/fedmix_backend',
    packages=[
        'fedmix_backend',
    ],
    install_requires=[
        'graphene>=2.1.8, <3',
        'flask>=1.1.2, <2',
        'flask-graphql>=2.0.1, <3',
    ],
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='fedmix-backend',
    entry_points={
        'console_scripts':
        ['fedmix-backend=fedmix_backend.fedmix_backend:main'],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    setup_requires=[
        'wheel',
        # dependency for `python setup.py test`
        'pytest-runner',
        # dependencies for `python setup.py build_sphinx`
        'sphinx',
        'sphinx_rtd_theme',
        'recommonmark'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-pylint',
    ],
    extras_require={
        'dev': ['prospector[with_pyroma]', 'yapf', 'isort'],
    },
)
