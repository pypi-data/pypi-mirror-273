from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.bulk_assembly_sequence_reference_polymer_type import BulkAssemblySequenceReferencePolymerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssemblySequenceReference")


@attr.s(auto_attribs=True, repr=False)
class BulkAssemblySequenceReference:
    """  """

    _polymer_type: Union[Unset, BulkAssemblySequenceReferencePolymerType] = UNSET
    _sequence_id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("polymer_type={}".format(repr(self._polymer_type)))
        fields.append("sequence_id={}".format(repr(self._sequence_id)))
        return "BulkAssemblySequenceReference({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        polymer_type: Union[Unset, int] = UNSET
        if not isinstance(self._polymer_type, Unset):
            polymer_type = self._polymer_type.value

        sequence_id = self._sequence_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if polymer_type is not UNSET:
            field_dict["polymerType"] = polymer_type
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_polymer_type() -> Union[Unset, BulkAssemblySequenceReferencePolymerType]:
            polymer_type = UNSET
            _polymer_type = d.pop("polymerType")
            if _polymer_type is not None and _polymer_type is not UNSET:
                try:
                    polymer_type = BulkAssemblySequenceReferencePolymerType(_polymer_type)
                except ValueError:
                    polymer_type = BulkAssemblySequenceReferencePolymerType.of_unknown(_polymer_type)

            return polymer_type

        try:
            polymer_type = get_polymer_type()
        except KeyError:
            if strict:
                raise
            polymer_type = cast(Union[Unset, BulkAssemblySequenceReferencePolymerType], UNSET)

        def get_sequence_id() -> Union[Unset, str]:
            sequence_id = d.pop("sequenceId")
            return sequence_id

        try:
            sequence_id = get_sequence_id()
        except KeyError:
            if strict:
                raise
            sequence_id = cast(Union[Unset, str], UNSET)

        bulk_assembly_sequence_reference = cls(
            polymer_type=polymer_type,
            sequence_id=sequence_id,
        )

        return bulk_assembly_sequence_reference

    @property
    def polymer_type(self) -> BulkAssemblySequenceReferencePolymerType:
        if isinstance(self._polymer_type, Unset):
            raise NotPresentError(self, "polymer_type")
        return self._polymer_type

    @polymer_type.setter
    def polymer_type(self, value: BulkAssemblySequenceReferencePolymerType) -> None:
        self._polymer_type = value

    @polymer_type.deleter
    def polymer_type(self) -> None:
        self._polymer_type = UNSET

    @property
    def sequence_id(self) -> str:
        """ API identifier for the nucleotide sequence. """
        if isinstance(self._sequence_id, Unset):
            raise NotPresentError(self, "sequence_id")
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value: str) -> None:
        self._sequence_id = value

    @sequence_id.deleter
    def sequence_id(self) -> None:
        self._sequence_id = UNSET
