from __future__ import annotations

import os
import re
import shutil
import typing

from .utils import create_missing_dirs

if typing.TYPE_CHECKING:
    from collections.abc import Iterable
    from re import Pattern


def avail_ar_exts() -> Iterable[str]:
    """Returns iterable of available archive extensions."""

    for fmt_name, fmt_exts, fmt_desc in shutil.get_unpack_formats():
        yield from fmt_exts


def is_ar(path: str) -> bool:
    """Returns whether given path is of archive file."""

    if not os.path.isfile(path):
        return False

    for fmt in avail_ar_exts():
        if path.endswith(fmt):
            return True
    return False


def strip_ext(path: str) -> str | None:
    """Strips extension from path to an archive file.
    Example:
    split_name_ext('/path/to/archive.zip') => '/path/to/archive'
    """

    for fmt in avail_ar_exts():
        if path.endswith(fmt):
            return path.removesuffix(fmt)
    return None  # for mypy


def ex_ar(path: str, prefix: str) -> None:
    """Extract archive file."""

    # split_name_ext will only return str
    # It would return None only if given filename is not
    # of an archive file. This would not happen as filename
    # filtering is done before this ex_ar is called.
    # So it is safe to type cast.
    ex_dir = typing.cast(str, strip_ext(path))
    create_missing_dirs(prefix, ex_dir)
    full_path = os.path.join(prefix, ex_dir)
    shutil.unpack_archive(filename, full_path)


def extract_archives(
    paths: Iterable[str],
    prefix: str,
    auto_del: bool,
    ignore_pattern: str,
    verbosity: int,
) -> None:
    """Wrapper function for ex_ar function."""

    ignore_pattern = re.compile(ignore_pattern)

    for path in paths:
        # ignore file
        if ignore_pattern.match(path):
            if verbosity:
                print(f"Ignoring path: {path}")
            continue

        # start extraction
        if verbosity:
            print(f"Starting extraction: {path}")

        ex_ar(path, prefix)

        # finish extraction
        if verbosity:
            print(f"Extracted file: {path}")

        # delete file
        if auto_del:
            os.remove(path)
            if verbosity:
                print(f"Delete file: {path}")
