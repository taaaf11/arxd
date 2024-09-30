from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from typing import Final

PROG_NAME: Final = "arxd"
PROG_NAME_DESIGN: Final = """\
┌─┐┬─┐─┐ ┬┌┬┐
├─┤├┬┘┌┴┬┘ ││
┴ ┴┴└─┴ └──┴┘\
"""

PROG_VER: Final = "2.0.0"

PROG_DESC: Final = f"""\
{PROG_NAME_DESIGN}

Extract (and delete) archive files under present working directory.\
"""

PROG_AUTHOR: Final = "Muhammad Altaaf <taafuuu@gmail.com>"

PROG_VER_INFO: Final = f"""\
{PROG_NAME_DESIGN}

{PROG_NAME} version: {PROG_VER}.
Written by:
  {PROG_AUTHOR}\
"""
