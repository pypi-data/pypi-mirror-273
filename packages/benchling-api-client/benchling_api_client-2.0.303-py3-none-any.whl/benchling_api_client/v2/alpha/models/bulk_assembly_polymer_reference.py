from typing import Union

from ..extensions import UnknownType
from ..models.bulk_assembly_protein_reference import BulkAssemblyProteinReference
from ..models.bulk_assembly_sequence_reference import BulkAssemblySequenceReference

BulkAssemblyPolymerReference = Union[BulkAssemblySequenceReference, BulkAssemblyProteinReference, UnknownType]
