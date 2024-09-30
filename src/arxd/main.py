from __future__ import annotations

import os
import sys

from .arxd import avail_ar_exts, extract_archives, is_ar
from .constants import PROG_VER_INFO
from .utils import parse_arguments


def main() -> None:
    args = parse_arguments()
    if args.exts:
        print("Supported archive formats: ", end="")
        print(", ".join(avail_ar_exts()))
        sys.exit(0)
    if args.version:
        print(PROG_VER_INFO)
        sys.exit(0)
    filenames = filter(
        is_ar,
        os.listdir(),
    )
    extract_archives(filenames, args.prefix, args.delete, args.ignore, args.verbosity)


if __name__ == "__main__":
    main()
