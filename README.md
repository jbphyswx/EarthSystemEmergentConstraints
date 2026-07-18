# EarthSystemEmergentConstraints

A **catalog of emergent-constraint definitions** for the Earth system.

Many papers have proposed emergent constraints: claimed relationships between an
observable / present-day quantity \(X\) and a projection / sensitivity quantity
\(Y\). This repository stores those claims in a structured, versioned library so
they can be listed, cited, compared, and reused as a benchmark resource.

## What this package does

- Stores structured definitions of published constraints (TOML + JSON Schema)
- Describes \(X\), \(Y\), and the claimed relationship (prose / optional LaTeX / optional Lean)
- Records citations and Hall-style assessment metadata
- Provides Julia and Python clients to **load, validate, and query** the catalog
- Optionally tags quantities with controlled vocabularies (e.g. CMIP variable names)

## What this package does *not* do

- Run climate models or read NetCDF
- Fit regressions or compute constrained probability distributions
- Assume CMIP (or any specific ensemble) as a runtime dependency
- Implement diagnostic pipelines

Ensembles named in a record (e.g. CMIP5) are **claim provenance** — where a
constraint was proposed or discussed — not a requirement to load model data.

## Layout

| Path | Role |
|------|------|
| [`schema/`](schema/) | JSON Schema for constraint and collection records |
| [`lib/constraints/registry/`](lib/constraints/registry/) | One TOML file per constraint (`<uuid>.toml`) |
| [`lib/constraints/collections/`](lib/constraints/collections/) | Named lists of aliases (e.g. `starter`) |
| [`julia/EarthSystemEmergentConstraints.jl/`](julia/EarthSystemEmergentConstraints.jl/) | Julia load / validate / query API |
| [`python/earth_system_emergent_constraints/`](python/earth_system_emergent_constraints/) | Python load / validate / query API |
| [`docs/`](docs/) | Concepts, schema reference, contributor guide |

## Quick start (Julia)

```julia
using EarthSystemEmergentConstraints

reg = load_registry()
c = reg["hall_qu_2006_snow_albedo"]
c.status
c.predictor.units
c.relationship.description
c.citation.doi

collection = load_collection("starter")
```

Set `ESEC_DATA_ROOT` to the repository root if the package cannot find `lib/`
automatically (e.g. editable checkout).

## Quick start (Python)

```python
from earth_system_emergent_constraints import load_registry, load_collection

reg = load_registry()
c = reg["hall_qu_2006_snow_albedo"]
print(c.status, c.predictor.units, c.citation.doi)

collection = load_collection("starter")
```

## Adding a constraint

See [`docs/adding_a_constraint.md`](docs/adding_a_constraint.md).

## License

MIT — see [`LICENSE`](LICENSE).
