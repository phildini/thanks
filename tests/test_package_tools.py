#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test for the package tools for extracting funding metadata"""

from collections import namedtuple
import os
import sys
from textwrap import dedent
import unittest

from ddt import ddt, data, unpack
import pkg_resources

import thanks.package_tools as ptools

# Add the mock packages in test/fixtures to sys.path
package_fixture_paths = os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 'fixtures')
sys.path.append(package_fixture_paths)

DistTestCase = namedtuple(
    'DistTestCase',
    ['description', 'dist', 'expected_path'],
)

DistMetadataPathTestCases = (
    DistTestCase(
        description='''
        Create a short egg-info name.
        ''',
        dist=pkg_resources.EggInfoDistribution(
            location= '/path/to/dist',
            project_name='crunchy-frog',
            version="0.1",
            py_version=None,
            platform=None,
        ),
        expected_path='/path/to/dist/crunchy_frog-0.1.egg-info/PKG-INFO'
    ),
    DistTestCase(
        description='''
        Ignores platform with no py_version
        ''',
        dist=pkg_resources.EggInfoDistribution(
            location= '/path/to/dist',
            project_name='crunchy-frog',
            version="0.1",
            py_version=None,
            platform='foo',
        ),
        expected_path='/path/to/dist/crunchy_frog-0.1.egg-info/PKG-INFO'
    ),
    DistTestCase(
        description='''
        Includes py version
        ''',
        dist=pkg_resources.EggInfoDistribution(
            location= '/path/to/dist',
            project_name='crunchy-frog',
            version="0.1",
            py_version='3.6',
            platform=None,
        ),
        expected_path='/path/to/dist/crunchy_frog-0.1-py3.6.egg-info/PKG-INFO'
    ),
    DistTestCase(
        description='''
        Create a short egg name.
        ''',
        dist=pkg_resources.Distribution(
            location= '/path/to/dist',
            project_name='crunchy-frog',
            version="0.1",
            py_version=None,
            platform=None,
        ),
        expected_path='/path/to/dist/crunchy_frog-0.1.egg/EGG-INFO/PKG-INFO'
    ),
    DistTestCase(
        description='''
        Create a short dist info name
        ''',
        dist=pkg_resources.DistInfoDistribution(
            location= '/path/to/dist',
            project_name='crunchy-frog',
            version="0.1",
            py_version=None,
            platform=None,
        ),
        expected_path='/path/to/dist/crunchy_frog-0.1.dist-info/METADATA'
    ),
)


@ddt
class TestPackageTools(unittest.TestCase):

    def test_get_local_funding_metadata_from_name(self):
        package_name = u'mosw'
        project_funding_url = ptools.get_local_funding_metadata(package_name)

        self.assertEqual(
            project_funding_url,
            'http://ministry-of-silly-walks.python/fundme'
        )

    @data(*DistMetadataPathTestCases)
    def test_generate_egg_project_location(self, tc):
        path = ptools.get_local_dist_metadata_filepath(tc.dist)

        self.assertEqual(path, tc.expected_path)

    def test_metadata_parsing(self):
        metadata_file = dedent("""
        Author: The Black Night
        Maintainer: King Authur
        Project-URL: Funding, https://monty.python/rabbits
        """)
        expected_metadata = {
            "author": "The Black Night",
            "maintainer": "King Authur",
            "funding_url": "https://monty.python/rabbits"
        }

        metadata = ptools.parse_metadata(metadata_file)

        self.assertEqual(metadata, expected_metadata)


if __name__ == '__main__':
    unittest.main()
