This is a library of known constraints.

Each constraint is represnted in YAML form (or should it be TOML)

Each has a (ideally unique) plain text title, alias, uuid, description, bibtex-like fields.
If applicable the constraint can store additional metadata (e.g. CMIP variables involved, equations in LEAN format)

Each constraint is stored in registry/<uuid>.toml
It is symlinked to in library/<library_name>.toml
