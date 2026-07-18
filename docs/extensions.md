# Extensions

Core packages only **load, validate, and query** catalog definitions.

## CMIP variable-name helpers (optional)

Constraint records may tag quantities:

```toml
[[variables]]
role = "predictor_input"
name = "tas"
vocab = "cmip"
```

Helpers check those names against a **sample** allow-list (not a full CMIP CV yet).
They do **not** download or diagnose model data.

### Python

```python
from earth_system_emergent_constraints import load_registry, validate_constraint_cmip_names

c = load_registry()["hall_qu_2006_snow_albedo"]
print(validate_constraint_cmip_names(c))  # [] if all sample-known
```

Optional extra group: `pip install -e ".[cmip]"` (reserved for a future pinned CV dependency).

### Julia

```julia
using EarthSystemEmergentConstraints
using EarthSystemEmergentConstraints.CMIPVocab

c = load_registry()["hall_qu_2006_snow_albedo"]
validate_constraint_cmip_names(c)
```

`ext/CMIPVocabExt.jl` is a placeholder for a future weakdep-based package extension.

## Explicitly not provided

- Applying constraints to ensemble \((x, y)\) tables
- NetCDF / ESGF / ESMValTool pipelines
- Statistical fitting or constrained PDFs

Those belong in other packages that may *read* this catalog.
