from __future__ import annotations

import json
from pathlib import Path

import pytest

from earth_system_emergent_constraints import load_collection, load_registry
from earth_system_emergent_constraints.paths import data_root, schema_dir

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


def test_data_root_has_registry():
    root = data_root()
    assert (root / "lib" / "constraints" / "registry").is_dir()


def test_load_registry_starter_set():
    reg = load_registry()
    assert len(reg) == 6
    assert "hall_qu_2006_snow_albedo" in reg

    c = reg["hall_qu_2006_snow_albedo"]
    assert c.status == "confirmed_candidate"
    assert c.citation.doi == "10.1029/2005GL025127"
    assert c.predictor.units == "%/K"
    assert "snow-albedo" in c.relationship.description
    assert reg[c.uuid].alias == c.alias

    contested = reg["cox_2018_psi_ecs"]
    assert contested.status == "contested"
    assert any(a.source == "Schlund2020" for a in contested.assessments)


def test_collections():
    reg = load_registry()
    starter = load_collection("starter", registry=reg)
    assert starter.name == "starter"
    assert len(starter.aliases) == 6
    assert len(starter.constraints) == 6

    ecs = load_collection("ecs", registry=reg)
    assert len(ecs.aliases) == 4
    assert all(c.target.short_name == "ECS" for c in ecs.constraints)


@pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
def test_registry_matches_json_schema():
    import tomllib

    root = data_root()
    schema = json.loads((schema_dir(root) / "constraint.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)

    for path in sorted((root / "lib" / "constraints" / "registry").glob("*.toml")):
        with path.open("rb") as f:
            data = tomllib.load(f)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        assert not errors, f"{path.name}: " + "; ".join(e.message for e in errors)


@pytest.mark.skipif(jsonschema is None, reason="jsonschema not installed")
def test_collections_match_json_schema():
    import tomllib

    root = data_root()
    schema = json.loads((schema_dir(root) / "collection.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)

    for path in sorted((root / "lib" / "constraints" / "collections").glob("*.toml")):
        with path.open("rb") as f:
            data = tomllib.load(f)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        assert not errors, f"{path.name}: " + "; ".join(e.message for e in errors)
