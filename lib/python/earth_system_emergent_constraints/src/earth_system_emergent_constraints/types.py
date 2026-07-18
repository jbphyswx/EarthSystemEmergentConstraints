from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional
from uuid import UUID


@dataclass(frozen=True)
class QuantitySpec:
    id: str
    short_name: str
    units: str
    description: str


@dataclass(frozen=True)
class Citation:
    doi: str
    year: Optional[int] = None
    authors: List[str] = field(default_factory=list)
    bibtex_key: Optional[str] = None


@dataclass(frozen=True)
class Relationship:
    description: str
    latex: Optional[str] = None
    lean: Optional[str] = None


@dataclass(frozen=True)
class HallAssessment:
    plausible_mechanism: Optional[bool] = None
    mechanism_verified: Optional[bool] = None
    out_of_sample_ok: Optional[bool] = None
    notes: Optional[str] = None


@dataclass(frozen=True)
class AssessmentEntry:
    source: str
    verdict: str
    notes: Optional[str] = None


@dataclass(frozen=True)
class VariableTag:
    role: str
    name: str
    vocab: Optional[str] = None


@dataclass(frozen=True)
class ConstraintNotes:
    caveats: List[str] = field(default_factory=list)
    related_aliases: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Constraint:
    schema_version: str
    uuid: UUID
    alias: str
    title: str
    status: str
    citation: Citation
    predictor: QuantitySpec
    target: QuantitySpec
    relationship: Relationship
    domain_realm: Optional[str] = None
    claim_discovered_in: List[str] = field(default_factory=list)
    claim_also_discussed_in: List[str] = field(default_factory=list)
    hall_assessment: Optional[HallAssessment] = None
    assessments: List[AssessmentEntry] = field(default_factory=list)
    variables: List[VariableTag] = field(default_factory=list)
    notes: ConstraintNotes = field(default_factory=ConstraintNotes)
    raw: Dict[str, Any] = field(default_factory=dict, repr=False)


@dataclass
class ConstraintRegistry:
    """In-memory index of registry constraints."""

    by_alias: Dict[str, Constraint]
    by_uuid: Dict[UUID, Constraint]
    root: str

    def __len__(self) -> int:
        return len(self.by_alias)

    def __contains__(self, key: object) -> bool:
        if isinstance(key, UUID):
            return key in self.by_uuid
        if isinstance(key, str):
            return key in self.by_alias
        return False

    def __getitem__(self, key: str | UUID) -> Constraint:
        if isinstance(key, UUID):
            return self.by_uuid[key]
        return self.by_alias[key]

    def __iter__(self) -> Iterator[Constraint]:
        return iter(self.by_alias.values())

    def aliases(self) -> List[str]:
        return sorted(self.by_alias)

    def uuids(self) -> List[UUID]:
        return sorted(self.by_uuid, key=str)


@dataclass(frozen=True)
class ConstraintCollection:
    name: str
    aliases: List[str]
    constraints: List[Constraint]
    description: Optional[str] = None
