"""
Useful functions for creating encryption schemes.
"""

# Explicit re-export of all functionalities, such that they can be imported properly. Following
# https://www.python.org/dev/peps/pep-0484/#stub-files and
# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
import platform
import sys
import warnings
from typing import Optional, TextIO, Type, Union

from .fixed_point import FixedPoint as FixedPoint
from .utils import lcm as lcm
from .utils import mod_inv as mod_inv
from .utils import pow_mod as pow_mod
from .utils import randprime as randprime


def custom_showwarning(  # pylint: disable=useless-type-doc
    message: Union[Warning, str],
    category: Type[Warning],
    _filename: str,
    _lineno: int,
    file: Optional[TextIO] = None,
    _line: Optional[str] = None,
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

try:
    import gmpy2
except ImportError:
    if platform.system() != "Windows":
        warnings.warn(
            "GMPY2 is not installed, however a significant performance improvement can be "
            "achieved by installing the GMPY2 library: "
            "'python -m pip install 'tno.mpc.encryption_schemes.utils[gmpy2]'",
        )

__version__ = "0.7.0"
