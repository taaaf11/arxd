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
    args: Namespace = typing.cast(Namespace, parse_arguments())
    ign_pat = re.compile(args.ignore)

    # get filenames of archives under present working directory
    filenames = filter(lambda filename: filter_ar(filename, ign_pat), os.listdir())

    if args.extract:
        extract_archives(filenames, args.prefix, args.delete)


if __name__ == "__main__":
    main()
