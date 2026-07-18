"""
Optional CMIP variable-name helpers.

This module is a **stub** for a future extension that validates `[[variables]]`
entries with `vocab = "cmip"` against a pinned CMIP controlled vocabulary.

It does not load model output, diagnose fields, or apply constraints.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Set

from .types import Constraint, VariableTag

# Minimal illustrative allow-list for tests/docs only — not a full CMIP CV.
_SAMPLE_CMIP_NAMES: Set[str] = {
    "tas",
    "tos",
    "hus",
    "hur",
    "snc",
    "rsds",
    "rsus",
    "rsdt",
    "rsutcs",
    "clt",
    "wa",
    "cVeg",
    "cSoil",
}


def cmip_variable_tags(constraint: Constraint) -> List[VariableTag]:
    """Return variable tags on ``constraint`` that declare ``vocab == \"cmip\"``."""
    return [v for v in constraint.variables if v.vocab == "cmip"]


def unknown_cmip_names(
    names: Iterable[str],
    *,
    allowlist: Sequence[str] | None = None,
) -> List[str]:
    """Return names not present in the (sample) CMIP allow-list.

    Replace ``allowlist`` with a pinned CV snapshot in a future release.
    """
    allowed = set(allowlist) if allowlist is not None else _SAMPLE_CMIP_NAMES
    return sorted({n for n in names if n not in allowed})


def validate_constraint_cmip_names(constraint: Constraint) -> List[str]:
    """Return unknown CMIP names tagged on ``constraint`` (empty if all known)."""
    names = [v.name for v in cmip_variable_tags(constraint)]
    return unknown_cmip_names(names)
