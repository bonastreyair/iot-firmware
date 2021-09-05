import argparse

from . import __version__


def cli():
    parser = argparse.ArgumentParser(
        prog="iot-firmware",
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
    parser.parse_args()
