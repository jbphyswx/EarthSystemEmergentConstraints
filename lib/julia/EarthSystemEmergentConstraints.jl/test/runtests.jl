using Test: Test
using EarthSystemEmergentConstraints: EarthSystemEmergentConstraints as ESEC
using UUIDs: UUIDs

Test.@testset "EarthSystemEmergentConstraints" begin
    root = ESEC.data_root()
    Test.@test isdir(joinpath(root, "lib", "constraints", "registry"))

    reg = ESEC.load_registry(root)
    Test.@test length(reg) == 6
    Test.@test "hall_qu_2006_snow_albedo" in ESEC.aliases(reg)

    c = reg["hall_qu_2006_snow_albedo"]
    Test.@test c.status == "confirmed_candidate"
    Test.@test c.citation.doi == "10.1029/2005GL025127"
    Test.@test c.predictor.units == "%/K"
    Test.@test occursin("snow-albedo", c.relationship.description)
    Test.@test c.uuid isa UUIDs.UUID
    Test.@test reg[c.uuid].alias == c.alias

    contested = reg["cox_2018_psi_ecs"]
    Test.@test contested.status == "contested"
    Test.@test any(a -> a.source == "Schlund2020", contested.assessments)

    starter = ESEC.load_collection("starter"; root=root, registry=reg)
    Test.@test starter.name == "starter"
    Test.@test length(starter.aliases) == 6
    Test.@test length(starter.constraints) == 6

    ecs = ESEC.load_collection("ecs"; root=root, registry=reg)
    Test.@test length(ecs.aliases) == 4
    Test.@test all(x -> x.target.short_name == "ECS", ecs.constraints)

    # Uniqueness already enforced by loader; re-check explicitly
    Test.@test length(unique(ESEC.aliases(reg))) == length(reg)
end
