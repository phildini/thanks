# -*- coding: utf-8 -*-

from humanfriendly.tables import format_pretty_table
import json
import os
import pip
import pprint
import requirements
from termcolor import colored, cprint
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib


json_file = ("{}/thanks.json".format(os.path.dirname(os.path.realpath(__file__))))
client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')


class Thanks():
    def __init__(self, debug=False):
        self.debug = debug
        self.data = {}
        with open(json_file, 'r') as j:
            print('Loading data about {}'.format(colored('contributors...', 'cyan')))
            self.data = json.load(j)
        self.give_thanks_to = {}
        self.local_installs = {}
        for package in pip.get_installed_distributions():
            self.local_installs[package.key] = package

    def find_package_roles(self, requirements_file):
        with open(requirements_file, 'r') as reqs:
            print('Scanning your {} file...'.format(colored('requirements', 'red')))
            for req in requirements.parse(reqs):
                self.update_give_thanks(req.name)
            if req.name in self.local_installs:
                for package in self.local_installs[req.name].requires():
                    self.update_give_thanks(package.key)
            if self.give_thanks_to:
                cprint(
                    'You depend on {} who would {}'.format(
                        colored('{} authors'.format(len(self.give_thanks_to)), 'cyan'),
                        colored('enjoy donations!', 'green'),
                    ), attrs=['bold'])
                table_data = []
                for contributor in self.give_thanks_to:
                    table_data.append(
                        [
                            colored(contributor, 'cyan'),
                            colored(self.give_thanks_to[contributor]['url'], 'green'),
                            colored(", ".join(self.give_thanks_to[contributor]['packages']), 'red'),
                        ]
                    )
                print(format_pretty_table(
                    data=table_data,
                    column_names=['Author', 'Where to thank', 'Packages'],
                    horizontal_bar=' ',
                    vertical_bar=' ',
                ))

    def update_give_thanks(self, package_name):
        if self.debug:
            print('Checking ', package_name)
        try:
            roles = client.package_roles(package_name)
            role_names = set(role[1] for role in roles)
            if self.debug:
                print('Checking role names: ', role_names)
            for name in role_names:
                if name in self.give_thanks_to:
                    self.give_thanks_to[name]['packages'].append(package_name)
                else:
                    if name in self.data:
                        self.give_thanks_to[name] = {
                            'url': self.data[name],
                            'packages': [package_name],
                        }
        except TypeError:
            pass
