from __future__ import annotations

import os
from pathlib import Path


def _is_data_root(path: Path) -> bool:
    return (path / "lib" / "constraints" / "registry").is_dir()


def _find_data_root(start: Path) -> Path | None:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if _is_data_root(candidate):
            return candidate
    return None


def data_root() -> Path:
    """Return the repository root that contains ``lib/constraints/``.

    Resolution order:
    1. ``ESEC_DATA_ROOT``
    2. Walk upward from this package looking for ``lib/constraints/registry``
    3. Walk upward from the current working directory
    """
    env = os.environ.get("ESEC_DATA_ROOT")
    if env:
        env_path = Path(env).expanduser().resolve()
        if _is_data_root(env_path):
            return env_path
        raise FileNotFoundError(
            f"ESEC_DATA_ROOT={env_path} does not contain lib/constraints/registry"
        )

    # .../src/earth_system_emergent_constraints/paths.py
    # -> package dir -> src -> earth_system_emergent_constraints (python pkg root)
    # -> python -> monorepo root
    here = Path(__file__).resolve()
    python_pkg_root = here.parents[2]  # .../python/earth_system_emergent_constraints
    monorepo = python_pkg_root.parent.parent  # .../EarthSystemEmergentConstraints
    if _is_data_root(monorepo):
        return monorepo

    found = _find_data_root(here)
    if found is not None:
        return found

    found = _find_data_root(Path.cwd())
    if found is not None:
        return found

    raise FileNotFoundError(
        "Could not locate ESEC data root (directory containing lib/constraints/registry). "
        "Set environment variable ESEC_DATA_ROOT to the EarthSystemEmergentConstraints repo root."
    )


def registry_dir(root: Path | None = None) -> Path:
    return (root or data_root()) / "lib" / "constraints" / "registry"


def collections_dir(root: Path | None = None) -> Path:
    return (root or data_root()) / "lib" / "constraints" / "collections"


def schema_dir(root: Path | None = None) -> Path:
    return (root or data_root()) / "schema"
