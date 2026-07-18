# Schema reference

Canonical schemas:

- [`schema/constraint.schema.json`](../schema/constraint.schema.json)
- [`schema/collection.schema.json`](../schema/collection.schema.json)

Records are authored as **TOML** under `lib/constraints/registry/<uuid>.toml`
and must satisfy the constraint schema. Collections list aliases only.

## Constraint: required fields

| Field | Notes |
|-------|--------|
| `schema_version` | SemVer string, currently `"0.1.0"` |
| `uuid` | RFC 4122 UUID; filename must be `<uuid>.toml` |
| `alias` | Stable snake_case machine id |
| `title` | Human title |
| `status` | `proposed` \| `contested` \| `confirmed_candidate` \| `withdrawn` |
| `citation.doi` | DOI string |
| `predictor` | `id`, `short_name`, `units`, `description` |
| `target` | same shape as predictor |
| `relationship.description` | Prose description of the claimed relation |
| assessment | `hall_assessment` and/or non-empty `assessments` |

## Optional fields

| Field | Notes |
|-------|--------|
| `domain.realm` | Free-form realm label |
| `claim_provenance` | Where the claim was proposed/discussed (labels only) |
| `relationship.latex` / `relationship.lean` | Optional formalization strings (unchecked) |
| `[[variables]]` | Optional tags: `role`, `name`, optional `vocab` |
| `notes.caveats` / `notes.related_aliases` | Human notes |

## Why there is no `relationship.form`

Published constraints use many functional forms (or none that are simple).
Classifying forms as `linear | log_linear | custom` would either be wrong or
useless for a **definition catalog**. Describe the relation; do not force an enum.

## Collections

```toml
name = "starter"
description = "..."
aliases = ["hall_qu_2006_snow_albedo", "..."]
```

Aliases must exist in the registry. No git symlinks.

## Validation

CI and local tests parse every registry/collection TOML and check it against
the JSON Schema (Python + `jsonschema`). Julia/Python loaders also enforce
required keys and unique aliases/UUIDs.
