# -*- coding: utf-8 -*-

"""Console script for thanks."""

import click
from .thanks import find_package_roles


@click.command()
@click.argument('requirements', default='requirements.txt', type=click.Path(exists=True))
def main(requirements):
    """Console script for thanks."""
    find_package_roles(requirements)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
