# -*- coding: utf-8 -*-
from __future__ import print_function

from collections import namedtuple
from humanfriendly.tables import format_pretty_table
import json
import logging
import os
import requirements
import requests
import termcolor
import toml
from termcolor import colored

from . import package_tools


logger = logging.getLogger("thanks")

JSON_FILE = ("{}/thanks.json".format(os.path.dirname(os.path.realpath(__file__))))

ProjectData = namedtuple('ProjectData', ['name', 'funding_link', 'authors'])


class Thanks():
    def __init__(self, debug=False):
        self.debug = debug
        self.give_thanks_to = {}

    def package(self, package_name):
        logger.debug("Checking {}".format(package_name))
        package_data = (self._get_local_data(package_name)
                        or self._get_remote_data(package_name))
        if package_data:
            self.give_thanks_to[package_name] = package_data

    def requirements_list(self, requirements_list):
        print('Scanning your {} file...'.format(colored('requirements', 'red')))
        reqs = [
            next(requirements.parse(r))
            for r in requirements_list.splitlines()
            if r != ""
        ]
        for req in reqs:
            self.package(req.name)

    def pipfile(self, pipfile):
        project_data = toml.loads(pipfile)
        reqs = []
        reqs += list(project_data.get("packages", {}).keys())
        reqs += list(project_data.get("dev-packages", {}).keys())
        for req in reqs:
            self.package(req)

    def _get_local_data(self, project_name):
        try:
            metadata = package_tools.get_local_metadata(project_name)
            funding_link = metadata.get('funding_url', '')
            authors = metadata.get('author', '')
            if not any([funding_link, authors]):
                return None

            data = ProjectData(
                name=project_name,
                funding_link=funding_link,
                authors=authors,
            )
        except KeyError:
            data = None
        except package_tools.MetaDataNotFound:
            data = None
        return data

    def _get_remote_data(self, project_name):
        url_format = 'https://pypi.org/pypi/{}/json'.format
        try:
            resp = requests.get(url_format(project_name))
            project_data = resp.json()
            data = ProjectData(
                name=project_name,
                funding_link=project_data['info'].get('funding_url', ''),
                authors=project_data['info'].get('author', '')
            )
        except requests.exceptions.ConnectionError:
            data = None
        except json.decoder.JSONDecodeError:
            data = None
        return data

    def _generate_output(self, colored_output=True):
        def _uncolored(text, *args, **kwargs):
            return text

        colored = termcolor.colored if colored_output else _uncolored

        lines = []
        lines.append(
            colored('You depend on {} who would {}'.format(
                colored('{} authors'.format(len(self.give_thanks_to)), 'cyan'),
                colored('enjoy donations!', 'green'),
                ),
                attrs=['bold']
            )
        )

        colorized_data = [
            ProjectData(
                name=colored(pd.name, 'cyan'),
                funding_link=colored(pd.funding_link, 'green'),
                authors=colored(pd.authors, 'yellow'),
            )
            for pd in self.give_thanks_to.values()
        ]

        lines.append(format_pretty_table(
            data=colorized_data,
            column_names=['Project', 'Where to thank', 'Authors'],
            horizontal_bar=' ',
            vertical_bar=' ',
        ))

        lines.append(colored(
                ''.join([
                    "If you see projects with ",
                    colored("MISSING FUNDING INFORMATION ", "red"),
                    "then why not submit a pull request ",
                    "the project repository asking the author to ",
                    colored("ADD A 'FUNDING' PROJECT_URL ", "yellow"),
                    "to the projects setup.py"
                ]),
                attrs=['bold']
        ))

        return '\n'.join(lines)

    def __str__(self, colored_output=True):
        return self._generate_output(colored_output)
