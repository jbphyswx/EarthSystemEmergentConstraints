# Constraint library

This directory holds the curated catalog of emergent-constraint definitions.

## Layout

| Path | Contents |
|------|----------|
| `registry/` | One TOML file per constraint, named `<uuid>.toml` |
| `collections/` | Named lists of constraint aliases (no git symlinks) |

## Format

Records are **TOML**, validated against [`../../schema/constraint.schema.json`](../../schema/constraint.schema.json).

Each record has (at minimum):

- Identity: `uuid`, `alias`, `title`, `status`
- `citation` with a DOI
- `predictor` and `target` quantity definitions
- `relationship.description`
- An assessment block (`hall_assessment` and/or `assessments`)

Optional `[[variables]]` entries may tag quantity inputs with a vocabulary
(e.g. `vocab = "cmip"`). That is metadata only — this library does not load models.

## Collections

Prefer `collections/<name>.toml` listing aliases over symlink forests. See
[`collections/starter.toml`](collections/starter.toml).
