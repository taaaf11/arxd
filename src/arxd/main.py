# #####################################################
# Name: arxd
# Author: Muhammad Altaaf
# Contact: taafuuu@gmail.com
# Descriptions: Extract and delete archive files
# present in present working directory.
# #####################################################

from __future__ import annotations

import os
import typing
from argparse import Namespace

from .arxd import is_ar, extract_archives
from .utils import parse_arguments


def main() -> None:
    args: Namespace = typing.cast(Namespace, parse_arguments())

    # get filenames of archives under present working directory
    filenames = filter(lambda filename: is_ar(filename), os.listdir())

    if args.extract:
        extract_archives(filenames, args.prefix, args.delete)


if __name__ == "__main__":
    main()
