# -*- coding: utf-8 -*-

import json
import os
import pprint
import requirements
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
        data = json.load(j)
    with open(requirements_file, 'r') as reqs:
        for req in requirements.parse(reqs):
            roles = client.package_roles(req.name)
            role_names = set(role[1] for role in roles)
            for name in role_names:
                if name in give_thanks_to:
                    give_thanks_to[name]['packages'].append(req.name)
                else:
                    if name in data:
                        give_thanks_to[name] = {'url': data[name], 'packages': [req.name]}
        for contributor in give_thanks_to:
            print(
                "{} contributes to {}, support them at {}".format(
                    contributor,
                    ",".join(give_thanks_to[contributor]['packages']),
                    give_thanks_to[contributor]['url'],
                ),
            )
