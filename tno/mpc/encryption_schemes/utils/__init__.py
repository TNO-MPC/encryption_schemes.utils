"""
Useful functions for creating encryption schemes.
"""

# Explicit re-export of all functionalities, such that they can be imported properly. Following
# https://www.python.org/dev/peps/pep-0484/#stub-files and
# https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-no-implicit-reexport
from .fixed_point import FixedPoint as FixedPoint
from .utils import lcm as lcm
from .utils import mod_inv as mod_inv
from .utils import pow_mod as pow_mod
from .utils import randprime as randprime

__version__ = "0.6.1"
