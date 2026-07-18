"""
    EarthSystemEmergentConstraints

Load, validate, and query the curated catalog of emergent-constraint definitions.
The catalog lives under `lib/constraints/` at the repository root (or under
`ESEC_DATA_ROOT`). This package does not run models or apply statistical constraints.
"""
module EarthSystemEmergentConstraints

using TOML: TOML
using UUIDs: UUIDs

export QuantitySpec, Citation, Relationship, HallAssessment, AssessmentEntry
export VariableTag, ConstraintNotes, Constraint, ConstraintRegistry, ConstraintCollection
export data_root, load_registry, load_collection, load_constraint
export aliases, uuids

include("types.jl")
include("paths.jl")
include("load.jl")
include("CMIPVocab.jl")

end # module
