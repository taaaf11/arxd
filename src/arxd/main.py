# #####################################################
# Name: arxd
# Author: Muhammad Altaaf
# Contact: taafuuu@gmail.com
# Descriptions: Extract and delete archive files
# present in present working directory.
# #####################################################

from __future__ import annotations

import functools
import os
import re

from .arxd import extract_archives, filter_ar
from .utils import parse_arguments


def main() -> None:
    args = parse_arguments()
    ignore_pattern = re.compile(args.ignore)

    filter_f = functools.partial(filter_ar, ignore_pattern=ignore_pattern)

    filenames = filter(
        filter_f,
        os.listdir(),
    )

    extract_archives(filenames, args.prefix, args.delete)


if __name__ == "__main__":
    main()
