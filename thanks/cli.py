# -*- coding: utf-8 -*-

"""Console script for thanks."""

import click
from .thanks import Thanks


@click.command()
@click.argument('requirements', default='requirements.txt', type=click.Path(exists=True))
@click.option('--debug', is_flag=True, help='Set debug mode')
def main(requirements, debug):
    """Console script for thanks."""
    with open(requirements, 'r') as fh:
        requirements = fh.read().strip().split()
    Thanks(debug=debug).find_project_details(requirements)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
