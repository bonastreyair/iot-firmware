import argparse
from typing import List
from typing import Optional

from . import __version__


def cli(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        prog="iot-firmware",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {__version__}",
        help="show program's version number and exit",
    )
    parser.add_argument(
        "-c",
        "--config",
        help="path to the configuration",
    )
    parser.parse_args(args)
