"""
Module that verifies compliance of the gmpy2 library and sets the result in
USE_GMPY2.

If gmpy2 is installed and the version is compliant with the current library,
set USE_GMPY2 to True. Otherwise, USE_GMPY2 is False.
"""


import re
import sys
import warnings

from packaging.specifiers import SpecifierSet
from packaging.version import parse

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, requires, version
else:
    from importlib_metadata import PackageNotFoundError, requires, version

SPECIFIER_OPERATOR = "===|==|!=|~=|<=|>=|<|>"
SPECIFIER_REGEX = rf"(?:{SPECIFIER_OPERATOR})\s*[\w\.\*]*"
SPECIFIER_SET_REGEX = rf"(?:{SPECIFIER_REGEX})(?:[\s,]*{SPECIFIER_REGEX})*"

# Import gmpy2 to improve efficiency (for larger integers), if available.
gmpy2_version = None
try:
    gmpy2_version = parse(version("gmpy2"))
except PackageNotFoundError:
    warnings.warn(
        "GMPY2 is not installed, however a significant performance improvement can be "
        "achieved by installing the GMPY2 library: "
        "'python -m pip install tno.mpc.encryption_schemes.utils[gmpy]'",
    )

USE_GMPY2 = False
if gmpy2_version is not None:
    DEPS = ";".join(requires(".".join(__name__.split(".")[:-1])))  # type: ignore[arg-type]
    gmpy2_spec_pattern = re.compile(
        f"gmpy2[^=~!<>]*?(?P<specs>({SPECIFIER_SET_REGEX}))"
    )
    gmpy2_spec_match = gmpy2_spec_pattern.search(DEPS)
    if gmpy2_spec_match is None:
        raise ValueError("Failed to extract optional gmpy2 version specifiers.")
    gmpy2_spec = SpecifierSet(gmpy2_spec_match.group("specs"))
    if gmpy2_version in gmpy2_spec:
        USE_GMPY2 = True
    else:
        warnings.warn(
            f"Efficiency gain is supported for gmpy2{gmpy2_spec}. Detected gmpy2 version "
            f"{gmpy2_version}. Fallback to non-gmpy2 support."
        )
