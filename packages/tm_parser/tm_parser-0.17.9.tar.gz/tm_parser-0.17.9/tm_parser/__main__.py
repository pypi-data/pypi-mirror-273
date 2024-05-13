"""
parser.py

from a troopmaster scout individual history report of all items, parse out
all kinds of scout information
"""

import sys

import click

from tm_parser import Parser
from objexplore import explore as objexplore

version = "0.17.9"


@click.command()
@click.option("-v", "--version", "get_version", is_flag=True)
@click.option(
    "-t",
    "--output-type",
    default="yaml",
    help="output type, options are yaml (default), toml, and json",
)
@click.option("-o", "--outfile", help='output filename, default is "output')
@click.argument(
    "infile",
    type=click.File("rb"),
    required=False,
)
@click.option("-e", "--explore", is_flag=True, help="open object explorer")
def main(output_type=None, outfile=None, infile=None, get_version=False, explore=False):
    """takes INFILE and outputs troopmaster data converted to standard out or to OUTFILE"""
    if get_version:
        print(f"tmparse version {version}")
        sys.exit()
    if not outfile:
        if not output_type:
            output_type = "json"
    elif outfile.endswith("json"):
        output_type = "json"
    elif outfile.endswith("yaml"):
        output_type = "yaml"
    elif outfile.endswith("toml"):
        output_type = "toml"

    print(infile)
    parser = Parser(infile=infile, outfile=outfile, file_format=output_type)

    if explore:
        objexplore(parser.scouts)
    elif outfile:
        parser.dump()
    else:
        print(parser.dumps())


if __name__ == "__main__":
    main()
