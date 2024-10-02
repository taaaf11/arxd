from __future__ import annotations

import functools
import os
import re
import shutil
import typing

from rich.console import Console

from .utils import create_missing_dirs

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from .config import Config


def avail_ar_exts() -> Iterable[str]:
    """Returns iterable of available archive extensions."""

    for fmt_name, fmt_exts, fmt_desc in shutil.get_unpack_formats():
        yield from fmt_exts


def is_ar(path: str) -> bool:
    """Returns whether given path is of archive file."""

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
    shutil.unpack_archive(path, full_path)


def extract_archives(paths: Sequence[str], config: Config) -> None:
    """Wrapper function for ex_ar function."""

    def add_blank_line(path: str, paths: Sequence[str]):
        if path is not paths[-1]:
            print()

    add_blank_line = functools.partial(add_blank_line, paths=paths)

    compiled_pattern = re.compile(config.ignore_pattern)
    console = Console()

    for path in paths:
        # ignore file
        if compiled_pattern.match(path):
            if config.verbosity or config.dry_run:
                console.print(f"Ignoring path: {path}", style="bold red")
            add_blank_line(path)
            continue

        if config.verbosity or config.dry_run:
            extracted_path = os.path.join(config.prefix, strip_ext(path))
            console.print(
                f'Extracting [bold yellow]"{path}"[/bold yellow] '
                f'to [bold yellow]"{extracted_path}"[/bold yellow]'
            )
        if not config.dry_run:
            ex_ar(path, config.prefix)

        # finish extraction
        if config.verbosity or config.dry_run:
            console.print(f"Extracted file: [bold green]{path}[/bold green]")

        # delete file
        if config.auto_del:
            if not config.dry_run:
                os.remove(path)
            if config.verbosity or config.dry_run:
                console.print(f"Deleted file: [bold cyan]{path}[/bold cyan]")

        add_blank_line(path)
