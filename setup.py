#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6',
    'humanfriendly>=4',
    'requirements-parser>=0.2',
    'termcolor>=1',
    'setuptools>=',
    'requests>=2',
    'toml'
]

setup_requirements = [
    "pytest-runner"
]

test_requirements = [
    "pytest",
    'ddt',
]

setup(
    name='thanks',
    version='0.0.8',
    description="Finding ways to fund the packages you use.",
    long_description=readme + '\n\n' + history,
    author="Philip James",
    author_email='phildini@phildini.net',
    url='https://github.com/phildini/thanks',
    project_urls={
        'Funding': 'https://patreon.com/phildini',
        'Source': 'https://github.com/phildini/thanks',
        'Tracker': 'https://github.com/phildini/thanks/issues',
    },
    packages=find_packages(include=['thanks']),
    entry_points={
        'console_scripts': [
            'thanks=thanks.cli:main',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='thanks',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
