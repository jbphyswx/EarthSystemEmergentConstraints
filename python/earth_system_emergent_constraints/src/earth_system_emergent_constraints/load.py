from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional
from uuid import UUID

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib  # type: ignore[attr-defined]
    except ModuleNotFoundError:  # pragma: no cover
        import tomli as tomllib  # type: ignore[no-redef]

from .paths import collections_dir, data_root, registry_dir
from .types import (
    AssessmentEntry,
    Citation,
    Constraint,
    ConstraintCollection,
    ConstraintNotes,
    ConstraintRegistry,
    HallAssessment,
    QuantitySpec,
    Relationship,
    VariableTag,
)

_REQUIRED_STATUSES = frozenset(
    {"proposed", "contested", "confirmed_candidate", "withdrawn"}
)


def _require(d: Mapping[str, Any], key: str, ctx: str) -> Any:
    if key not in d:
        raise KeyError(f'Missing required key "{key}" in {ctx}')
    return d[key]


def _str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"Expected list, got {type(value)!r}")
    return [str(v) for v in value]


def _parse_quantity(d: Mapping[str, Any], ctx: str) -> QuantitySpec:
    return QuantitySpec(
        id=str(_require(d, "id", ctx)),
        short_name=str(_require(d, "short_name", ctx)),
        units=str(_require(d, "units", ctx)),
        description=str(_require(d, "description", ctx)),
    )


def _parse_citation(d: Mapping[str, Any]) -> Citation:
    year = d.get("year")
    return Citation(
        doi=str(_require(d, "doi", "citation")),
        year=int(year) if year is not None else None,
        authors=_str_list(d.get("authors", [])),
        bibtex_key=str(d["bibtex_key"]) if d.get("bibtex_key") is not None else None,
    )


def _parse_relationship(d: Mapping[str, Any]) -> Relationship:
    return Relationship(
        description=str(_require(d, "description", "relationship")),
        latex=str(d["latex"]) if d.get("latex") is not None else None,
        lean=str(d["lean"]) if d.get("lean") is not None else None,
    )


def _parse_hall(d: Any) -> Optional[HallAssessment]:
    if d is None:
        return None
    if not isinstance(d, Mapping):
        raise TypeError("hall_assessment must be a table")
    return HallAssessment(
        plausible_mechanism=d.get("plausible_mechanism"),
        mechanism_verified=d.get("mechanism_verified"),
        out_of_sample_ok=d.get("out_of_sample_ok"),
        notes=str(d["notes"]) if d.get("notes") is not None else None,
    )


def _parse_assessments(value: Any) -> List[AssessmentEntry]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("assessments must be an array of tables")
    out: List[AssessmentEntry] = []
    for i, entry in enumerate(value):
        if not isinstance(entry, Mapping):
            raise TypeError(f"assessments[{i}] must be a table")
        out.append(
            AssessmentEntry(
                source=str(_require(entry, "source", f"assessments[{i}]")),
                verdict=str(_require(entry, "verdict", f"assessments[{i}]")),
                notes=str(entry["notes"]) if entry.get("notes") is not None else None,
            )
        )
    return out


def _parse_variables(value: Any) -> List[VariableTag]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("variables must be an array of tables")
    out: List[VariableTag] = []
    for i, entry in enumerate(value):
        if not isinstance(entry, Mapping):
            raise TypeError(f"variables[{i}] must be a table")
        out.append(
            VariableTag(
                role=str(_require(entry, "role", f"variables[{i}]")),
                name=str(_require(entry, "name", f"variables[{i}]")),
                vocab=str(entry["vocab"]) if entry.get("vocab") is not None else None,
            )
        )
    return out


def _parse_notes(d: Any) -> ConstraintNotes:
    if d is None:
        return ConstraintNotes()
    if not isinstance(d, Mapping):
        raise TypeError("notes must be a table")
    return ConstraintNotes(
        caveats=_str_list(d.get("caveats", [])),
        related_aliases=_str_list(d.get("related_aliases", [])),
    )


def _validate(d: Mapping[str, Any], path: str) -> None:
    for key in (
        "schema_version",
        "uuid",
        "alias",
        "title",
        "status",
        "citation",
        "predictor",
        "target",
        "relationship",
    ):
        if key not in d:
            raise KeyError(f'Missing required key "{key}" in {path}')
    status = str(d["status"])
    if status not in _REQUIRED_STATUSES:
        raise ValueError(f'Invalid status "{status}" in {path}')
    has_hall = "hall_assessment" in d and d["hall_assessment"] is not None
    assessments = d.get("assessments")
    has_assess = isinstance(assessments, list) and len(assessments) > 0
    if not (has_hall or has_assess):
        raise ValueError(f"Need hall_assessment and/or assessments in {path}")


def constraint_from_dict(d: Mapping[str, Any], *, path: str = "<memory>") -> Constraint:
    _validate(d, path)
    domain = d.get("domain") or {}
    realm = None
    if isinstance(domain, Mapping):
        realm = str(domain["realm"]) if domain.get("realm") is not None else None

    provenance = d.get("claim_provenance") or {}
    if not isinstance(provenance, Mapping):
        raise TypeError(f"claim_provenance must be a table in {path}")

    return Constraint(
        schema_version=str(d["schema_version"]),
        uuid=UUID(str(d["uuid"])),
        alias=str(d["alias"]),
        title=str(d["title"]),
        status=str(d["status"]),
        domain_realm=realm,
        citation=_parse_citation(d["citation"]),
        claim_discovered_in=_str_list(provenance.get("discovered_in", [])),
        claim_also_discussed_in=_str_list(provenance.get("also_discussed_in", [])),
        predictor=_parse_quantity(d["predictor"], "predictor"),
        target=_parse_quantity(d["target"], "target"),
        relationship=_parse_relationship(d["relationship"]),
        hall_assessment=_parse_hall(d.get("hall_assessment")),
        assessments=_parse_assessments(d.get("assessments")),
        variables=_parse_variables(d.get("variables")),
        notes=_parse_notes(d.get("notes")),
        raw=dict(d),
    )


def load_constraint(path: str | Path) -> Constraint:
    path = Path(path)
    with path.open("rb") as f:
        data = tomllib.load(f)
    return constraint_from_dict(data, path=str(path))


def load_registry(root: str | Path | None = None) -> ConstraintRegistry:
    root_path = Path(root).resolve() if root is not None else data_root()
    directory = registry_dir(root_path)
    if not directory.is_dir():
        raise FileNotFoundError(f"Registry directory not found: {directory}")

    by_alias: Dict[str, Constraint] = {}
    by_uuid: Dict[UUID, Constraint] = {}

    for file in sorted(directory.glob("*.toml")):
        c = load_constraint(file)
        expected = f"{c.uuid}.toml"
        if file.name != expected:
            raise ValueError(f'Registry file "{file.name}" must be named "{expected}"')
        if c.alias in by_alias:
            raise ValueError(f'Duplicate alias "{c.alias}" in registry')
        if c.uuid in by_uuid:
            raise ValueError(f'Duplicate uuid "{c.uuid}" in registry')
        by_alias[c.alias] = c
        by_uuid[c.uuid] = c

    return ConstraintRegistry(by_alias=by_alias, by_uuid=by_uuid, root=str(root_path))


def load_collection(
    name: str,
    *,
    root: str | Path | None = None,
    registry: ConstraintRegistry | None = None,
) -> ConstraintCollection:
    root_path = Path(root).resolve() if root is not None else data_root()
    reg = registry if registry is not None else load_registry(root_path)
    path = collections_dir(root_path) / f"{name}.toml"
    if not path.is_file():
        raise FileNotFoundError(f"Collection not found: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    if "name" not in data or "aliases" not in data:
        raise KeyError(f"Collection {path} must have name and aliases")
    if str(data["name"]) != name:
        raise ValueError(
            f'Collection file name "{name}" does not match name field "{data["name"]}"'
        )

    aliases = _str_list(data["aliases"])
    if not aliases:
        raise ValueError(f'Collection "{name}" has empty aliases')
    if len(set(aliases)) != len(aliases):
        raise ValueError(f'Collection "{name}" has duplicate aliases')

    constraints = []
    for alias in aliases:
        if alias not in reg:
            raise KeyError(f'Collection "{name}" references unknown alias "{alias}"')
        constraints.append(reg[alias])

    description = data.get("description")
    return ConstraintCollection(
        name=str(data["name"]),
        aliases=aliases,
        constraints=constraints,
        description=str(description) if description is not None else None,
    )
