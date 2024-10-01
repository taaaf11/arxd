from __future__ import annotations

import os
import typing
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .actions import CustomHelpAction
from .constants import PROG_DESC, PROG_NAME

if typing.TYPE_CHECKING:
    from argparse import Namespace


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DESC,
        add_help=False,
        formatter_class=RawDescriptionHelpFormatter,
    )
    add_arg = parser.add_argument

    add_arg(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="Delete files after extraction is completed.",
    )
    add_arg(
        "-p",
        "--prefix",
        type=str,
        default="",
        help="Set prefix. Default is <current directory>/",
    )
    add_arg(
        "-i",
        "--ignore",
        metavar="PATTERN",
        type=str,
        default="~^",  # does not match anything
        help="Ignore filenames matching given PATTERN.",
    )
    add_arg(
        "--exts",
        default=False,
        action="store_true",
        help="List supported archive filename extensions.",
    )
    add_arg(
        "-v",
        "--verbose",
        dest="verbosity",
        action="store_true",
        help="Be verbose.",
    )
    add_arg(
        "-V",
        "--version",
        action="store_true",
        help="Print version info.",
    )
    add_arg(
        "-h",
        "--help",
        action=CustomHelpAction,
    )

    return parser.parse_args()


def create_missing_dirs(prefix: str, ex_dir: str) -> None:
    def mkdir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    if prefix:
        mkdir(prefix)
    mkdir(os.path.join(prefix, ex_dir))
