from __future__ import annotations

import os
import sys

from .arxd import avail_ar_exts, extract_archives, is_ar
from .config import Config
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
        lambda path: os.path.isfile(path) and is_ar(path),
        os.listdir(),
    )
    config = Config(
        args.prefix,
        args.delete,
        args.ignore,
        args.verbosity,
    )
    extract_archives(filenames, config)


if __name__ == "__main__":
    main()
