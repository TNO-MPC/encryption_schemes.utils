from __future__ import annotations

class PackageNotFoundError(ModuleNotFoundError): ...

def requires(distribution_name: str) -> list[str]: ...
def version(distribution_name: str) -> str: ...
