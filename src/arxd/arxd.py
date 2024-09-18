"""
Name: arxd
Author: Muhammad Altaaf
Contact: taafuuu@gmail.com
Description: A script to extract (and delete if asked) all the archive files present in cwd.
"""


import os
import shutil
import sys
import typing
from argparse import ArgumentParser
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

# a prefix is made up of two parts
# one part: the parent directory (specified with -p cli option)
# second part: the filename itself
# the name of file is always part of prefix, even if parent directory
# is not specified


@dataclass(frozen=True)
class _Config:
    """A class for easy storage and access to configuration."""

    prefix: str = None
    auto_del: bool = False


def get_avail_ar_exts() -> Iterable[str]:
    """Returns iterable of available archive formats."""

    for fmt_name, fmt_ext, fmt_desc in shutil.get_unpack_formats():
        yield from fmt_ext


def is_ar(filename: str) -> bool:
    """Returns whether given filename is name of an archive."""

    for fmt in get_avail_ar_exts():
        if filename.endswith(fmt):
            return True
    return False


def split_ext(filename: str) -> bool:
    """Split archive filename into two parts: filename without
    extension, the extension. Don't confuse it with os.path.splitext.
    """

    for fmt in get_avail_ar_exts():
        if filename.endswith(fmt):
            return filename.removesuffix(fmt)


def create_missing_dirs(prefix: str):
    """Create missing directories."""

    psplit = prefix.split("/")

    isdir = os.path.isdir
    mkdir = os.mkdir

    if len(psplit) == 2:
        parent_dir, cont_dir = psplit
    else:
        parent_dir, cont_dir = "", psplit[0]

    if parent_dir:
        cont_dir_path = os.path.join(parent_dir, cont_dir)
        if not isdir(parent_dir):
            mkdir(parent_dir)
            mkdir(cont_dir_path)
        elif isdir(parent_dir) and not isdir(cont_dir_path):
            mkdir(cont_dir_path)
    else:
        if not isdir(cont_dir):
            mkdir(cont_dir)


def ex_ar(filename: str, prefix: str | None = None) -> bool:
    """Extract archive file represented by filename."""

    ex_dir: str = split_ext(filename)
    if prefix:
        prefix = os.path.join(prefix, ex_dir)
    else:
        prefix = ex_dir

    # create missing directories if they don't already exist
    create_missing_dirs(prefix)
    shutil.unpack_archive(filename, prefix)


def extract_archives(filenames: Iterable[str], prefix: str, auto_del: bool):
    """Wrapper function for ex_ar function."""

    for filename in filenames:
        ex_ar(filename, prefix)
        if auto_del:
            os.remove(filename)


def filter_ar(filename: str) -> bool:
    """Returns whether given file name is of archive file.
    """

    return os.path.isfile(filename) and is_ar(filename)


def main():
    # get filenames of archives under pwd
    filenames = filter(lambda filename: filter_ar(filename), os.listdir())

    parser = ArgumentParser()
    parser.add_argument(
        "-e",
        "--extract",
        action="store_true",
        default=False,
        help="Start extraction. None of the options have effect without this option.",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        default=False,
        help="Delete files after extraction is completed.",
    )
    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        help="Set prefix. Default is <current directory>/<filename>/",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    prefix = None
    auto_del = False

    if args.delete:
        auto_del = True
    if args.prefix:
        prefix = args.prefix.strip("/")
    if args.extract:
        extract_archives(filenames, prefix, auto_del)


if __name__ == "__main__":
    main()
