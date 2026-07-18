"""Load, validate, and query the emergent-constraint catalog."""

from .paths import data_root
from .load import load_registry, load_collection, load_constraint
from .cmip_vocab import (
    cmip_variable_tags,
    unknown_cmip_names,
    validate_constraint_cmip_names,
)
from .types import (
    AssessmentEntry,
    Citation,
    Constraint,
    ConstraintCollection,
    ConstraintNotes,
    ConstraintRegistry,
    HallAssessment,
    QuantitySpec,
    Relationship,
    VariableTag,
)

__all__ = [
    "AssessmentEntry",
    "Citation",
    "Constraint",
    "ConstraintCollection",
    "ConstraintNotes",
    "ConstraintRegistry",
    "HallAssessment",
    "QuantitySpec",
    "Relationship",
    "VariableTag",
    "cmip_variable_tags",
    "data_root",
    "load_collection",
    "load_constraint",
    "load_registry",
    "unknown_cmip_names",
    "validate_constraint_cmip_names",
]

__version__ = "0.1.0"
