# -*- coding: utf-8 -*-

import json
import os
import pip
import pprint
import requirements
from termcolor import colored
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
            print("Loading data about contributors...")
            self.data = json.load(j)
        self.give_thanks_to = {}
        self.local_installs = {}
        for package in pip.get_installed_distributions():
            self.local_installs[package.key] = package

    def find_package_roles(self, requirements_file):
        with open(requirements_file, 'r') as reqs:
            print("Scanning your requirements file...")
            for req in requirements.parse(reqs):
                self.update_give_thanks(req.name)
            if req.name in self.local_installs:
                for package in self.local_installs[req.name].requires():
                    self.update_give_thanks(package.key)
            if self.give_thanks_to:
                print("Found the following contributors to support: \n")
                for contributor in self.give_thanks_to:
                    print(
                        "{} contributes to {}, support them at {}".format(
                            colored(contributor, 'blue'),
                            colored(",".join(self.give_thanks_to[contributor]['packages']), 'red'),
                            colored(self.give_thanks_to[contributor]['url'], 'green'),
                        )
                    )
                print("\n")

    def update_give_thanks(self, package_name):
        if self.debug:
            print("Checking ", package_name)
        try:
            roles = client.package_roles(package_name)
            role_names = set(role[1] for role in roles)
            if self.debug:
                print("Checking role names: ", role_names)
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
