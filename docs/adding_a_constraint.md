# Adding a constraint

## Checklist

1. Choose a stable `alias` (`snake_case`) and generate a new UUID.
2. Create `lib/constraints/registry/<uuid>.toml` (filename **must** match the UUID).
3. Fill required fields (see [schema.md](schema.md)).
4. Write an honest `status` and assessment block from the literature — do not invent verdicts.
5. Optionally add `[[variables]]` with `vocab = "cmip"` when CMIP names are relevant.
6. Add the alias to any collections that should include it (e.g. `collections/starter.toml`).
7. Add a BibTeX entry to `lib/bib/references.bib` if useful.
8. Run schema/loader tests (see below).

## Template

```toml
schema_version = "0.1.0"
uuid = "00000000-0000-0000-0000-000000000000"
alias = "author_year_short_name"
title = "Human-readable title"
status = "proposed"

[citation]
doi = "10.xxxx/xxxxx"
year = 20xx
authors = ["Last, F."]
bibtex_key = "AuthorYear"

[predictor]
id = "semantic_predictor_id"
short_name = "X"
units = "..."
description = "..."

[target]
id = "semantic_target_id"
short_name = "Y"
units = "..."
description = "..."

[relationship]
description = """
Describe the claimed relation in prose.
"""

[hall_assessment]
plausible_mechanism = true
mechanism_verified = false
out_of_sample_ok = false
notes = "..."

[[assessments]]
source = "AuthorYear"
verdict = "proposed"
notes = "..."
```

## Local checks

From the repo root:

```bash
export ESEC_DATA_ROOT="$PWD"

# Python
cd python/earth_system_emergent_constraints
python -m pip install -e ".[dev]"
pytest -q

# Julia
julia --project=julia/EarthSystemEmergentConstraints.jl -e 'using Pkg; Pkg.test()'
```
