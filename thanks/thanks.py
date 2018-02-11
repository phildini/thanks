# -*- coding: utf-8 -*-

import json
import os
import pprint
import requirements
from termcolor import colored
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib


json_file = ("{}/thanks.json".format(os.path.dirname(os.path.realpath(__file__))))
client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')


def find_package_roles(requirements_file):
    data = {}
    give_thanks_to = {}
    with open(json_file, 'r') as j:
        print("Loading data about contributors...")
        data = json.load(j)
    with open(requirements_file, 'r') as reqs:
        print("Scanning your requirements file...")
        for req in requirements.parse(reqs):
            roles = client.package_roles(req.name)
            role_names = set(role[1] for role in roles)
            for name in role_names:
                if name in give_thanks_to:
                    give_thanks_to[name]['packages'].append(req.name)
                else:
                    if name in data:
                        give_thanks_to[name] = {'url': data[name], 'packages': [req.name]}
        if give_thanks_to:
            print("Found the following contributors to support: \n")
            for contributor in give_thanks_to:
                print(
                    "{} contributes to {}, support them at {}".format(
                        colored(contributor, 'blue'),
                        colored(",".join(give_thanks_to[contributor]['packages']), 'red'),
                        colored(give_thanks_to[contributor]['url'], 'green'),
                    )
                )
            print("\n")
