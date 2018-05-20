# -*- coding: utf-8 -*-

from collections import namedtuple
from humanfriendly.tables import format_pretty_table
import json
import os
import requirements
import requests
from termcolor import colored, cprint


JSON_FILE = ("{}/thanks.json".format(os.path.dirname(os.path.realpath(__file__))))

ProjectData = namedtuple('ProjectData', ['name', 'funding_link', 'authors'])


class Thanks():
    def __init__(self, debug=False):
        self.debug = debug
        self.data = self.load_local_project_data()
        self.give_thanks_to = {}

    def load_local_project_data(self):
        print('Loading data about {}'.format(colored('contributors...', 'cyan')))
        with open(JSON_FILE, 'r') as fh:
            data = json.load(fh)
            for project_name in data.keys():
                authors = ', '.join(data[project_name].get('authors', []))
                data[project_name]['authors'] = authors
        return data

    def find_project_details(self, requirements_list):
        print('Scanning your {} file...'.format(colored('requirements', 'red')))
        reqs = [
            next(requirements.parse(r))
            for r in requirements_list
        ]
        for req in reqs:
            self.update_give_thanks(req.name)
        self._display_thanks()

    def _display_thanks(self):
        if self.give_thanks_to:
            cprint(
                'You depend on {} who would {}'.format(
                    colored('{} authors'.format(len(self.give_thanks_to)), 'cyan'),
                    colored('enjoy donations!', 'green'),
                ), attrs=['bold'])
            colorized_data = [
                ProjectData(
                    name=colored(pd.name, 'cyan'),
                    funding_link=colored(pd.funding_link, 'green'),
                    authors=colored(pd.authors, 'yellow'),
                )
                for pd in self.give_thanks_to.values()
            ]

            print(format_pretty_table(
                data=colorized_data,
                column_names=['Project', 'Where to thank', 'Authors'],
                horizontal_bar=' ',
                vertical_bar=' ',
            ))

    def get_local_data(self, project_name):
        if project_name in self.data:
            data = ProjectData(
                name=project_name,
                funding_link=self.data[project_name]['url'],
                authors=self.data[project_name]['authors']
            )
        else:
            data = None
        return data

    def get_remote_data(self, project_name):
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

    def update_give_thanks(self, package_name):
        if self.debug:
            print('Checking ', package_name)
        package_data = self.get_local_data(package_name) or self.get_remote_data(package_name)
        if package_data:
            self.give_thanks_to[package_name] = package_data
