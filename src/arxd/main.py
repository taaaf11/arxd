# #####################################################
# Name: arxd
# Author: Muhammad Altaaf
# Contact: taafuuu@gmail.com
# Descriptions: Extract and delete archive files
# present in present working directory.
# #####################################################

from __future__ import annotations

import os
import re
import typing
from argparse import Namespace

from .arxd import extract_archives, filter_ar
from .utils import parse_arguments


def main() -> None:
    # parse_arguments function returns None only if no command
    # line argument is given. In that case, it exits the program.
    # So it is safe to type cast its return value
    args: Namespace = typing.cast(Namespace, parse_arguments())
    ignore_pattern = re.compile(args.ignore)

    filenames = filter(
        lambda filename: filter_ar(filename, ignore_pattern),
        os.listdir(),
    )

    if args.extract:
        extract_archives(filenames, args.prefix, args.delete)


if __name__ == "__main__":
    main()
