# Emergent constraints — concepts

## What this catalog stores

An **emergent constraint** (Hall et al., 2019) is a claimed relationship between:

- an **observable / present-day quantity** \(X\) (the *predictor*), and
- a **projection / sensitivity quantity** \(Y\) (the *target*),

such that knowledge of \(X\) can inform \(Y\). The claim is typically discovered by
comparing many Earth-system predictions; those ensembles are **provenance of the
claim**, not something this package executes.

Each catalog entry records:

1. Identity (`alias`, `uuid`, `title`, `status`)
2. Definitions of \(X\) and \(Y\)
3. A prose (and optional LaTeX / Lean) description of the relationship
4. Citations
5. Assessment metadata (Hall-style indicators and literature verdicts)

## Status values

| Status | Meaning |
|--------|---------|
| `proposed` | Published claim; confirmation incomplete |
| `contested` | Serious doubts (e.g. failed out-of-sample tests) |
| `confirmed_candidate` | Strong mechanism + supportive assessment literature |
| `withdrawn` | Authors or community no longer endorse the claim |

Hall et al. use a proposed→confirmed ladder. No EC is ever fully “proven”;
`confirmed_candidate` is the strongest label this schema uses.

## Assessment fields

`hall_assessment` mirrors Hall et al. (2019) confirmation indicators:

- `plausible_mechanism`
- `mechanism_verified`
- `out_of_sample_ok`

Additional `[[assessments]]` rows cite specific papers (e.g. Caldwell 2018,
Schlund 2020) without inventing new science in code.

## What relationships are *not*

The schema does **not** require a relationship “form” enum (`linear`, etc.).
Relationships are described. Optional `latex` / `lean` strings are documentation
aids, not dispatch keys.

## Out of scope

This package does not fit regressions, load NetCDF, or apply constraints to
ensemble tables. See [extensions.md](extensions.md) for optional CMIP *name*
helpers only.
