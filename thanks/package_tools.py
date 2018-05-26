from functools import reduce
from itertools import chain, takewhile
import os
import pkg_resources
import re


class MetaDataNotFound(Exception):
    pass


def get_local_dist(package_name):
    working_set = dict(
        (dist.project_name, dist) for dist in pkg_resources.WorkingSet()
    )

    return working_set[package_name]


def get_dist_metadata(dist):
    metadata_path = get_local_dist_metadata_filepath(dist)
    with open(metadata_path) as fh:
        metadata = parse_metadata(fh.read())
    return metadata


def get_funding_data(metadata):
    return metadata.get('funding_url')


def get_local_dist_metadata_filepath(dist):
    # Dist filename syntax
    # name ["-" version ["-py" pyver ["-" required_platform]]] "." ext
    # https://setuptools.readthedocs.io/en/latest/formats.html#filename-embedded-metadata
    filename = ''.join(chain(*takewhile(lambda x: x[1], (
        ('',    pkg_resources.to_filename(pkg_resources.safe_name(dist.project_name))),
        ('-',   pkg_resources.to_filename(pkg_resources.safe_version(dist.version))),
        ('-py', dist.py_version),
        ('-',   dist.platform),
    ))))
    if isinstance(dist, pkg_resources.EggInfoDistribution):
        ext = 'egg-info'
        metadata_file = 'PKG-INFO'
    elif isinstance(dist, pkg_resources.DistInfoDistribution):
        ext = 'dist-info'
        metadata_file = 'METADATA'
    elif isinstance(dist, pkg_resources.Distribution):
        ext = os.path.join('egg', 'EGG-INFO')
        metadata_file = 'PKG-INFO'
    else:
        ext = None
        metadata_file = None

    filename = '{}.{}'.format(filename, ext)
    path = os.path.join(dist.location, filename, metadata_file)

    if ext:
        return path
    else:
        return None


metadata_patterns = re.compile(r"""
    (\s*Author:\s+(?P<author>.*)\s*)?                      # Author
    (\s*Maintainer:\s+(?P<maintainer>.+)\s*)?              # Maintainer
    (\s*Project-URL:\sFunding,\s+(?P<funding_url>.+)\s*)?  # Funding URL
""", re.VERBOSE)


def get_line_metadata(line):
    return metadata_patterns.search(line).groupdict()


def filter_empty_metadata(metadata):
    return dict((k, v) for k, v in metadata.items() if v)


def parse_metadata(metadata):
    metadata = (
        filter_empty_metadata(get_line_metadata(line))
        for line in metadata.splitlines()
    )
    metadata = [m for m in metadata if m]
    metadata = reduce(
        lambda x, y: dict((k, v) for k, v in chain(x.items(), y.items())),
        metadata,
        {},
    )
    return metadata


def get_local_metadata(package_name):
    try:
        dist = get_local_dist(package_name)
        metadata = get_dist_metadata(dist)
    except FileNotFoundError:
        # No metadata.json file locally
        raise MetaDataNotFound()

    return metadata


def get_local_funding_metadata(package_name):
    try:
        metadata = get_local_metadata(package_name)
        funding_url = get_funding_data(metadata)
    except KeyError:
        # Package not available locally,
        # or there isn't a 'Funding' entry in the project_urls
        raise MetaDataNotFound()

    return funding_url
