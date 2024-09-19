from __future__ import annotations

import os
import typing

from .arxd import is_ar
from .utils import parse_arguments, extract_archives

if typing.TYPE_CHECKING:
    from argparse import Namespace


def main() -> None:
    args: Namespace = typing.cast(Namespace, parse_arguments())

    # get filenames of archives under present working directory
    filenames = filter(lambda filename: is_ar(filename), os.listdir())

    if args.extract:
        extract_archives(filenames, args.prefix, args.delete)


if __name__ == "__main__":
    main()
