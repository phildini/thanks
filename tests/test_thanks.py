#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `thanks` package."""

import os
import sys
import unittest
from click.testing import CliRunner

from thanks import cli, Thanks

# Add the mock packages in test/fixtures to sys.path
package_fixture_paths = os.path.join(os.path.dirname(
                            os.path.realpath(__file__)), 'fixtures')
sys.path.append(package_fixture_paths)


class TestThanks(unittest.TestCase):
    """Tests for `thanks` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_thanks_package(self):
        thanks = Thanks()

        thanks.package("crunchy-frog")

        output = thanks.rocks(colored_output=False)

        assert "You depend on 1 authors" in output
        assert "crunchy-frog                    Kenneth Reitz" in output

    def test_thanks_requirements_list(self):
        thanks = Thanks()

        thanks.requirements_list(["crunchy-frog"])

        output = thanks.rocks(colored_output=False)

        assert "You depend on 1 authors" in output
        assert "crunchy-frog                    Kenneth Reitz" in output
