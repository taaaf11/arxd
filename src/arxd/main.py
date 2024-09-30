from __future__ import annotations

import os

from .arxd import extract_archives, is_ar
from .utils import parse_arguments


def main() -> None:
    args = parse_arguments()
    filenames = filter(
        is_ar,
        os.listdir(),
    )
    extract_archives(filenames, args.prefix, args.delete, args.ignore, args.verbosity)


if __name__ == "__main__":
    main()
