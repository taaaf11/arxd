from __future__ import annotations

import os
import sys
import typing
from argparse import ArgumentParser

if typing.TYPE_CHECKING:
    from argparse import Namespace
    from collections.abc import Iterable


def parse_arguments() -> Namespace | None:
    parser = ArgumentParser()
    add_arg = parser.add_argument

    add_arg(
        "-e",
        "--extract",
        action="store_true",
        default=False,
        help="Start extraction. None of the options have "
        "effect without this option.",
    )
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
        default=None,
        help="Set prefix. Default is <current directory>/",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def create_missing_dirs(prefix, ex_dir) -> None:
    def mkdir(path):
        if not os.path.exists(path):
            os.mkdir(path)

    if prefix:
        mkdir(prefix)
    mkdir(ex_dir)
