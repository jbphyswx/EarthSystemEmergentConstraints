const Optional{T} = Union{T,Nothing}

"""Semantic definition of a predictor or target quantity."""
struct QuantitySpec
    id::AbstractString
    short_name::AbstractString
    units::AbstractString
    description::AbstractString
end

struct Citation
    doi::String
    year::Optional{Int}
    authors::AbstractVector{<:AbstractString}
    bibtex_key::Optional{<:AbstractString}
end

struct Relationship
    description::AbstractString
    latex::Optional{<:AbstractString}
    lean::Optional{<:AbstractString}
end

struct HallAssessment
    plausible_mechanism::Optional{Bool}
    mechanism_verified::Optional{Bool}
    out_of_sample_ok::Optional{Bool}
    notes::Optional{<:AbstractString}
end

struct AssessmentEntry
    source::AbstractString
    verdict::AbstractString
    notes::Optional{<:AbstractString}
end

struct VariableTag
    role::AbstractString
    name::AbstractString
    vocab::Union{AbstractString,Nothing}
end

struct ConstraintNotes{CT <: AbstractVector{<:AbstractString}, RT <: AbstractVector{<:AbstractString}}
    caveats::CT
    related_aliases::CT
end

"""A single catalog record for a published emergent constraint."""
struct Constraint
    schema_version::AbstractString
    uuid::UUIDs.UUID
    alias::AbstractString
    title::AbstractString
    status::AbstractString
    domain_realm::Optional{<:AbstractString}
    citation::Citation
    claim_discovered_in::AbstractVector{<:AbstractString}
    claim_also_discussed_in::AbstractVector{<:AbstractString}
    predictor::QuantitySpec
    target::QuantitySpec
    relationship::Relationship
    hall_assessment::Optional{HallAssessment}
    assessments::AbstractVector{AssessmentEntry}
    variables::AbstractVector{VariableTag}
    notes::ConstraintNotes
    raw::AbstractDict{<:AbstractString,<:Any}
end

"""In-memory index of all registry constraints, keyed by alias and UUID."""
struct ConstraintRegistry
    by_alias::AbstractDict{<:AbstractString,Constraint}
    by_uuid::AbstractDict{UUIDs.UUID,Constraint}
    root::AbstractString
end

struct ConstraintCollection
    name::AbstractString
    description::Optional{<:AbstractString}
    aliases::AbstractVector{<:AbstractString}
    constraints::AbstractVector{Constraint}
end

Base.length(r::ConstraintRegistry) = length(r.by_alias)
Base.keys(r::ConstraintRegistry) = keys(r.by_alias)
Base.haskey(r::ConstraintRegistry, k::AbstractString) = haskey(r.by_alias, String(k))
Base.haskey(r::ConstraintRegistry, u::UUIDs.UUID) = haskey(r.by_uuid, u)

function Base.getindex(r::ConstraintRegistry, k::AbstractString)
    key = String(k)
    haskey(r.by_alias, key) || throw(KeyError(key))
    return r.by_alias[key]
end

function Base.getindex(r::ConstraintRegistry, u::UUIDs.UUID)
    haskey(r.by_uuid, u) || throw(KeyError(u))
    return r.by_uuid[u]
end

function Base.iterate(r::ConstraintRegistry, state...)
    return iterate(values(r.by_alias), state...)
end

aliases(r::ConstraintRegistry) = sort!(collect(keys(r.by_alias)))
uuids(r::ConstraintRegistry) = sort!(collect(keys(r.by_uuid)); by=string)
