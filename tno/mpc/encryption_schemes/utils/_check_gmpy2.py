"""
Module that verifies compliance of the gmpy2 library and sets the result in
USE_GMPY2.

If gmpy2 is installed and the version is compliant with the current library,
set USE_GMPY2 to True. Otherwise, USE_GMPY2 is False.
"""


import re
import warnings
from typing import Optional, Union

import packaging

try:
    from importlib.metadata import PackageNotFoundError, requires, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, requires, version  # type: ignore[misc]

from packaging.specifiers import SpecifierSet

SPECIFIER_OPERATOR = "===|==|!=|~=|<=|>=|<|>"
SPECIFIER_REGEX = f"(?:{SPECIFIER_OPERATOR})\s*[\w\.\*]*"
SPECIFIER_SET_REGEX = f"(?:{SPECIFIER_REGEX})(?:[\s,]*{SPECIFIER_REGEX})*"

# Import gmpy2 to improve efficiency (for larger integers), if available.
gmpy2_version: Optional[
    Union[packaging.version.Version, packaging.version.LegacyVersion]
] = None
try:
    gmpy2_version = packaging.version.parse(version("gmpy2"))
except PackageNotFoundError:
    warnings.warn(
        "GMPY2 is not installed, however a significant performance improvement can be "
        "achieved by installing the GMPY2 library: "
        "'python -m pip install 'tno.mpc.encryption_schemes.utils[gmpy]'",
    )

USE_GMPY2 = False
if gmpy2_version is not None:
    deps = ";".join(requires(".".join(__name__.split(".")[:-1])))  # type: ignore[arg-type]
    gmpy2_spec_pattern = re.compile(
        f"gmpy2[^=~!<>]*?(?P<specs>({SPECIFIER_SET_REGEX}))"
    )
    gmpy2_spec_match = gmpy2_spec_pattern.search(deps)
    if gmpy2_spec_match is None:
        raise ValueError(f"Failed to extract optional gmpy2 version specifiers.")
    gmpy2_spec = SpecifierSet(gmpy2_spec_match.group("specs"))
    if gmpy2_version in gmpy2_spec:
        USE_GMPY2 = True
    else:
        warnings.warn(
            f"Efficiency gain is supported for gmpy2{gmpy2_spec}. Detected gmpy2 version "
            f"{gmpy2_version}. Fallback to non-gmpy2 support."
        )
