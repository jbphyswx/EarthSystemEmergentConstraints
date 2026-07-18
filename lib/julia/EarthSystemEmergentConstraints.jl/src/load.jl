const _REQUIRED_STATUSES = Set(["proposed", "contested", "confirmed_candidate", "withdrawn"])

function _require_key(d::AbstractDict, key::AbstractString, ctx::AbstractString)
    haskey(d, key) || error("Missing required key \"$key\" in $ctx")
    return d[key]
end

function _as_string_vector(x)::Vector{String}
    x === nothing && return String[]
    x isa AbstractVector || error("Expected array, got $(typeof(x))")
    return String[string(v) for v in x]
end

function _parse_quantity(d::AbstractDict, ctx::AbstractString)::QuantitySpec
    return QuantitySpec(
        string(_require_key(d, "id", ctx)),
        string(_require_key(d, "short_name", ctx)),
        string(_require_key(d, "units", ctx)),
        string(_require_key(d, "description", ctx)),
    )
end

function _parse_citation(d::AbstractDict)::Citation
    year = get(d, "year", nothing)
    year_int = year === nothing ? nothing : Int(year)
    authors = _as_string_vector(get(d, "authors", String[]))
    bib = get(d, "bibtex_key", nothing)
    return Citation(
        string(_require_key(d, "doi", "citation")),
        year_int,
        authors,
        bib === nothing ? nothing : string(bib),
    )
end

function _parse_relationship(d::AbstractDict)::Relationship
    latex = get(d, "latex", nothing)
    lean = get(d, "lean", nothing)
    return Relationship(
        string(_require_key(d, "description", "relationship")),
        latex === nothing ? nothing : string(latex),
        lean === nothing ? nothing : string(lean),
    )
end

function _parse_hall(d)::Union{HallAssessment,Nothing}
    d === nothing && return nothing
    d isa AbstractDict || error("hall_assessment must be a table")
    notes = get(d, "notes", nothing)
    return HallAssessment(
        get(d, "plausible_mechanism", nothing),
        get(d, "mechanism_verified", nothing),
        get(d, "out_of_sample_ok", nothing),
        notes === nothing ? nothing : string(notes),
    )
end

function _parse_assessments(x)::Vector{AssessmentEntry}
    x === nothing && return AssessmentEntry[]
    x isa AbstractVector || error("assessments must be an array of tables")
    out = AssessmentEntry[]
    for (i, entry) in enumerate(x)
        entry isa AbstractDict || error("assessments[$i] must be a table")
        notes = get(entry, "notes", nothing)
        push!(
            out,
            AssessmentEntry(
                string(_require_key(entry, "source", "assessments[$i]")),
                string(_require_key(entry, "verdict", "assessments[$i]")),
                notes === nothing ? nothing : string(notes),
            ),
        )
    end
    return out
end

function _parse_variables(x)::Vector{VariableTag}
    x === nothing && return VariableTag[]
    x isa AbstractVector || error("variables must be an array of tables")
    out = VariableTag[]
    for (i, entry) in enumerate(x)
        entry isa AbstractDict || error("variables[$i] must be a table")
        vocab = get(entry, "vocab", nothing)
        push!(
            out,
            VariableTag(
                string(_require_key(entry, "role", "variables[$i]")),
                string(_require_key(entry, "name", "variables[$i]")),
                vocab === nothing ? nothing : string(vocab),
            ),
        )
    end
    return out
end

function _parse_notes(d)::ConstraintNotes
    d === nothing && return ConstraintNotes(String[], String[])
    d isa AbstractDict || error("notes must be a table")
    return ConstraintNotes(
        _as_string_vector(get(d, "caveats", String[])),
        _as_string_vector(get(d, "related_aliases", String[])),
    )
end

function _validate_constraint_dict!(d::AbstractDict, path::AbstractString)
    for key in ("schema_version", "uuid", "alias", "title", "status", "citation", "predictor", "target", "relationship")
        haskey(d, key) || error("Missing required key \"$key\" in $path")
    end
    status = string(d["status"])
    status in _REQUIRED_STATUSES || error("Invalid status \"$status\" in $path")
    has_hall = haskey(d, "hall_assessment")
    has_assess = haskey(d, "assessments") && d["assessments"] !== nothing && !isempty(d["assessments"])
    (has_hall || has_assess) || error("Need hall_assessment and/or assessments in $path")
    return nothing
end

"""Parse one constraint TOML dict into a `Constraint`."""
function constraint_from_dict(d::AbstractDict; path::AbstractString="<memory>")::Constraint
    _validate_constraint_dict!(d, path)

    domain = get(d, "domain", nothing)
    realm = nothing
    if domain isa AbstractDict
        r = get(domain, "realm", nothing)
        realm = r === nothing ? nothing : string(r)
    end

    provenance = get(d, "claim_provenance", Dict{String,Any}())
    if provenance === nothing
        provenance = Dict{String,Any}()
    end
    provenance isa AbstractDict || error("claim_provenance must be a table in $path")

    hall = _parse_hall(get(d, "hall_assessment", nothing))
    assessments = _parse_assessments(get(d, "assessments", nothing))

    return Constraint(
        string(d["schema_version"]),
        UUIDs.UUID(string(d["uuid"])),
        string(d["alias"]),
        string(d["title"]),
        string(d["status"]),
        realm,
        _parse_citation(d["citation"]),
        _as_string_vector(get(provenance, "discovered_in", String[])),
        _as_string_vector(get(provenance, "also_discussed_in", String[])),
        _parse_quantity(d["predictor"], "predictor"),
        _parse_quantity(d["target"], "target"),
        _parse_relationship(d["relationship"]),
        hall,
        assessments,
        _parse_variables(get(d, "variables", nothing)),
        _parse_notes(get(d, "notes", nothing)),
        Dict{String,Any}(string(k) => v for (k, v) in d),
    )
end

"""Load a single constraint TOML file."""
function load_constraint(path::AbstractString)::Constraint
    d = TOML.parsefile(path)
    return constraint_from_dict(d; path=path)
end

"""
    load_registry(root=data_root()) -> ConstraintRegistry

Load every `*.toml` file under `lib/constraints/registry/`.
"""
function load_registry(root::AbstractString=data_root())::ConstraintRegistry
    dir = registry_dir(root)
    isdir(dir) || error("Registry directory not found: $dir")

    by_alias = Dict{String,Constraint}()
    by_uuid = Dict{UUIDs.UUID,Constraint}()

    for file in sort(filter(f -> endswith(f, ".toml"), readdir(dir)))
        path = joinpath(dir, file)
        c = load_constraint(path)
        expected = "$(c.uuid).toml"
        file == expected || error("Registry file \"$file\" must be named \"$expected\"")
        haskey(by_alias, c.alias) && error("Duplicate alias \"$(c.alias)\" in registry")
        haskey(by_uuid, c.uuid) && error("Duplicate uuid \"$(c.uuid)\" in registry")
        by_alias[c.alias] = c
        by_uuid[c.uuid] = c
    end

    return ConstraintRegistry(by_alias, by_uuid, abspath(root))
end

"""
    load_collection(name; root=data_root(), registry=load_registry(root)) -> ConstraintCollection

Load `lib/constraints/collections/<name>.toml` and resolve aliases against the registry.
"""
function load_collection(
    name::AbstractString;
    root::AbstractString=data_root(),
    registry::ConstraintRegistry=load_registry(root),
)::ConstraintCollection
    path = joinpath(collections_dir(root), "$(name).toml")
    isfile(path) || error("Collection not found: $path")
    d = TOML.parsefile(path)
    haskey(d, "name") || error("Missing name in $path")
    haskey(d, "aliases") || error("Missing aliases in $path")
    string(d["name"]) == string(name) ||
        error("Collection file name \"$name\" does not match name field \"$(d["name"])\"")

    alias_list = _as_string_vector(d["aliases"])
    isempty(alias_list) && error("Collection \"$name\" has empty aliases")
    length(unique(alias_list)) == length(alias_list) ||
        error("Collection \"$name\" has duplicate aliases")

    constraints = Constraint[]
    for a in alias_list
        haskey(registry, a) || error("Collection \"$name\" references unknown alias \"$a\"")
        push!(constraints, registry[a])
    end

    desc = get(d, "description", nothing)
    return ConstraintCollection(
        string(d["name"]),
        desc === nothing ? nothing : string(desc),
        alias_list,
        constraints,
    )
end
