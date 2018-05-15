import json
import pkg_resources


class MetaDataNotFound(Exception):
    pass


def get_local_dist(package_name):
    working_set = dict(
        (dist.project_name, dist) for dist in pkg_resources.WorkingSet()
    )

    return working_set[package_name]


def get_dist_metadata(dist):
    metadata_path = '{}/{}-{}.dist-info/{}'.format(
        dist.location,
        dist.project_name,
        dist.parsed_version.public,
        'metadata.json',
    )
    with open(metadata_path) as fh:
        metadata = json.load(fh)
    return metadata


def get_funding_data(metadata):
        return (
            metadata['extensions']['python.details']['project_urls']['Funding']
        )


def get_local_funding_metadata(package_name):
    try:
        dist = get_local_dist(package_name)
        metadata = get_dist_metadata(dist)
        funding_url = get_funding_data(metadata)
    except FileNotFoundError:
        # No metadata.json file locally
        raise MetaDataNotFound()
    except KeyError:
        # Package not available locally,
        # or there isn't a 'Funding' entry in the project_urls
        raise MetaDataNotFound()

    return funding_url
