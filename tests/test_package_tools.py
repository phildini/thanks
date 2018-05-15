#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test for the package tools for extracting funding metadata"""

from builtins import open as og_open
import io
import json
import os
import sys
import unittest
import unittest.mock as mock

import thanks.package_tools as ptools

# Add the mock packages in test/fixtures to sys.path
package_fixture_paths = os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 'fixtures')
sys.path.append(package_fixture_paths)


class TestPakcageTools(unittest.TestCase):

    def test_get_local_funding_metadata_from_name(self):
        package_name = u'mosw'
        project_funding_url = ptools.get_local_funding_metadata(package_name)

        self.assertEqual(
            project_funding_url,
            'http://ministry-of-silly-walks.python/fundme'
        )


if __name__ == '__main__':
    unittest.main()