"""
    data_root() -> String

Return the repository root that contains `lib/constraints/`.

Resolution order:
1. Environment variable `ESEC_DATA_ROOT`
2. Walk upward from this package directory looking for `lib/constraints/registry`
3. Walk upward from the current working directory
"""
function data_root()::String
    env = get(ENV, "ESEC_DATA_ROOT", nothing)
    if env !== nothing && _is_data_root(env)
        return abspath(env)
    end

    pkg_dir = dirname(dirname(@__DIR__))  # .../julia/EarthSystemEmergentConstraints.jl -> .../julia
    monorepo = dirname(pkg_dir)           # .../EarthSystemEmergentConstraints
    if _is_data_root(monorepo)
        return monorepo
    end

    # Walk from package file location
    here = @__DIR__
    found = _find_data_root(here)
    found !== nothing && return found

    found = _find_data_root(pwd())
    found !== nothing && return found

    error(
        "Could not locate ESEC data root (directory containing lib/constraints/registry). " *
        "Set environment variable ESEC_DATA_ROOT to the EarthSystemEmergentConstraints repo root.",
    )
end

function _is_data_root(path::AbstractString)::Bool
    return isdir(joinpath(path, "lib", "constraints", "registry"))
end

function _find_data_root(start::AbstractString)
    dir = abspath(start)
    while true
        if _is_data_root(dir)
            return dir
        end
        parent = dirname(dir)
        parent == dir && return nothing
        dir = parent
    end
end

registry_dir(root::AbstractString=data_root()) =
    joinpath(root, "lib", "constraints", "registry")

collections_dir(root::AbstractString=data_root()) =
    joinpath(root, "lib", "constraints", "collections")

schema_dir(root::AbstractString=data_root()) = joinpath(root, "schema")
