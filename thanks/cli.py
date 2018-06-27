# -*- coding: utf-8 -*-

"""Console script for thanks."""
import logging

import click
from thanks.thanks import Thanks

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger("thanks")


@click.command()
@click.argument("package_name",
                nargs=-1)
@click.option("--requirements", "-r",
              multiple=True,
              type=click.File("r"))
# @click.option("--pipfile", "-p",
#               multiple=True,
#               type=click.File("r"))
# @click.option("--setuppy", "-s",
#               multiple=True,
#               type=click.File("r"))
# @click.option("--poetry", type=click.Path(exists=True))
# @click.option("--hatch", type=click.Path(exists=True))
@click.option("--debug/--no-debug", default=False, help='Set debug mode')
@click.option("--outfile", "-o",
              type=click.File("w"),
              default="-", help='Save output to file')
def main(package_name, requirements,
        #  pipfile, setuppy,
         debug, outfile):
    if debug:
        logger.level = logging.DEBUG
    thanks = Thanks(debug=debug)
    for p in package_name:
        thanks.package(p)
    for r in requirements:
        requirements_list = r.read().splitlines()
        thanks.requirements_list(requirements_list)
    # for p in pipfile:
    #     thanks.pipfile(p)

    outfile.write(thanks.rocks())


if __name__ == "__main__":
    import sys
    sys.exit(cli())
