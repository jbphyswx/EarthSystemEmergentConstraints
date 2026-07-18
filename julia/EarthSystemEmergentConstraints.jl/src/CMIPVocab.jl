"""
    EarthSystemEmergentConstraints.CMIPVocab

Stub helpers for optional CMIP variable-name tags on catalog records.

```julia
using EarthSystemEmergentConstraints
using EarthSystemEmergentConstraints.CMIPVocab
```

Does **not** load models or diagnose CMIP fields. The allow-list below is a
minimal sample for tests/docs — replace with a pinned CV snapshot later.
"""
module CMIPVocab

using ..EarthSystemEmergentConstraints: Constraint, VariableTag

const SAMPLE_CMIP_NAMES = Set([
    "tas", "tos", "hus", "hur", "snc", "rsds", "rsus", "rsdt", "rsutcs", "clt", "wa", "cVeg", "cSoil",
])

cmip_variable_tags(c::Constraint) = VariableTag[v for v in c.variables if v.vocab == "cmip"]

function unknown_cmip_names(names; allowlist=SAMPLE_CMIP_NAMES)
    allowed = Set(string(x) for x in allowlist)
    return sort!(unique(String[string(n) for n in names if !(string(n) in allowed)]))
end

function validate_constraint_cmip_names(c::Constraint)
    return unknown_cmip_names(v.name for v in cmip_variable_tags(c))
end

export cmip_variable_tags, unknown_cmip_names, validate_constraint_cmip_names

end # module
