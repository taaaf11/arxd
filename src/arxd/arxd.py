from __future__ import annotations

import os
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
    # of an archive file. So it is safe to type cast.
    ex_dir: str = typing.cast(str, split_name_ext(filename))
    create_missing_dirs(prefix, ex_dir)
    full_path = os.path.join(prefix, ex_dir)
    shutil.unpack_archive(filename, full_path)


def extract_archives(filenames: Iterable[str], prefix: str, auto_del: bool) -> None:
    """Wrapper function for ex_ar function."""

    for filename in filenames:
        ex_ar(filename, prefix)
        if auto_del:
            os.remove(filename)


def filter_ar(filename: str, ignore_pattern: Pattern) -> bool:
    """Returns True if given filename has an extension as
    given by avail_ar_exts and it does NOT match
    given compiled regex pattern (ignore_pattern).
    """

    return is_ar(filename) and not ignore_pattern.match(filename)
