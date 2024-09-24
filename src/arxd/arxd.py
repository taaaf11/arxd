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


def is_ar(filename: str) -> bool:
    """Returns whether given filename is of archive file."""

    if not os.path.isfile(filename):
        return False

    for fmt in avail_ar_exts():
        if filename.endswith(fmt):
            return True
    return False


def split_name_ext(filename: str) -> str | None:
    """Split archive filename into two parts:
    filename without extension, the extension.
    """

    for fmt in avail_ar_exts():
        if filename.endswith(fmt):
            return filename.removesuffix(fmt)
    return None  # for mypy


def ex_ar(filename: str, prefix: str) -> None:
    """Extract archive file."""

    # split_name_ext will only return str
    # It would return None only if given filename is not
    # of an archive file. This would not happen as filename
    # filtering is done before this ex_ar is called.
    # So it is safe to type cast.
    ex_dir = typing.cast(str, split_name_ext(filename))
    create_missing_dirs(prefix, ex_dir)
    full_path = os.path.join(prefix, ex_dir)
    shutil.unpack_archive(filename, full_path)


def extract_archives(
    filenames: Iterable[str],
    prefix: str,
    auto_del: bool,
    ignore_pattern: str,
    verbosity: int,
) -> None:
    """Wrapper function for ex_ar function."""

    ignore_pattern = re.compile(ignore_pattern)

    for filename in filenames:
        # ignore file
        if ignore_pattern.match(filename):
            if verbosity:
                print(f"Ignoring file: {filename}")
            continue

        # start extraction
        if verbosity:
            print(f"Starting extraction: {filename}")

        ex_ar(filename, prefix)

        # finish extraction
        if verbosity:
            print(f"Extracted file: {filename}")

        # delete file
        if auto_del:
            os.remove(filename)
            if verbosity:
                print(f"Delete file: {filename}")
