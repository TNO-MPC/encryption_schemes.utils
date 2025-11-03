"""
Root imports for the tno.mpc.encryption_schemes.utils package.
"""

# Explicit re-export of all functionalities, such that they can be imported properly. Following
# https://www.python.org/dev/peps/pep-0484/#stub-files and
# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
from __future__ import annotations

import sys
import warnings
from typing import TextIO

from tno.mpc.encryption_schemes.utils._check_gmpy2 import USE_GMPY2 as USE_GMPY2
from tno.mpc.encryption_schemes.utils.fixed_point import FixedPoint as FixedPoint
from tno.mpc.encryption_schemes.utils.utils import is_prime as is_prime
from tno.mpc.encryption_schemes.utils.utils import lcm as lcm
from tno.mpc.encryption_schemes.utils.utils import mod_inv as mod_inv
from tno.mpc.encryption_schemes.utils.utils import next_prime as next_prime
from tno.mpc.encryption_schemes.utils.utils import pow_mod as pow_mod
from tno.mpc.encryption_schemes.utils.utils import randprime as randprime


def custom_showwarning(  # pylint: disable=useless-type-doc
    message: Warning | str,
    category: type[Warning],
    _filename: str,
    _lineno: int,
    file: TextIO | None = None,
    _line: str | None = None,
) -> None:
    """
    Custom warning formatter and printer for python warnings. Prints category and message to
    output file, default stderr.

    :param message: Warning message, explaining the reason for the warning.
    :param category: Warning category.
    :param file: Optional location to write the warning to. If None we write to stderr.
    """
    print(f"{category.__name__}: {message}", file=file if file else sys.stderr)


warnings.showwarning = custom_showwarning  # type: ignore[assignment]

__version__ = "0.16.1"
