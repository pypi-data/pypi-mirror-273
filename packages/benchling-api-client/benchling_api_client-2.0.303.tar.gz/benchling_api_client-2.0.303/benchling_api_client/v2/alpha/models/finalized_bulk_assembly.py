from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.bulk_assembly_concatenation_method import BulkAssemblyConcatenationMethod
from ..models.bulk_assembly_constant_bin import BulkAssemblyConstantBin
from ..models.bulk_assembly_fragment_bin import BulkAssemblyFragmentBin
from ..models.bulk_assembly_fragment_shared import BulkAssemblyFragmentShared
from ..models.bulk_assembly_gibson_method import BulkAssemblyGibsonMethod
from ..models.bulk_assembly_golden_gate_method import BulkAssemblyGoldenGateMethod
from ..models.bulk_assembly_homology_method import BulkAssemblyHomologyMethod
from ..models.finalized_bulk_assembly_constructs import FinalizedBulkAssemblyConstructs
from ..types import UNSET, Unset

T = TypeVar("T", bound="FinalizedBulkAssembly")


@attr.s(auto_attribs=True, repr=False)
class FinalizedBulkAssembly:
    """  """

    _bins: Union[Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]] = UNSET
    _constructs: Union[Unset, FinalizedBulkAssemblyConstructs] = UNSET
    _fragments: Union[Unset, List[BulkAssemblyFragmentShared]] = UNSET
    _method: Union[
        Unset,
        BulkAssemblyGoldenGateMethod,
        BulkAssemblyGibsonMethod,
        BulkAssemblyHomologyMethod,
        BulkAssemblyConcatenationMethod,
        UnknownType,
    ] = UNSET

    def __repr__(self):
        fields = []
        fields.append("bins={}".format(repr(self._bins)))
        fields.append("constructs={}".format(repr(self._constructs)))
        fields.append("fragments={}".format(repr(self._fragments)))
        fields.append("method={}".format(repr(self._method)))
        return "FinalizedBulkAssembly({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bins: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._bins, Unset):
            bins = []
            for bins_item_data in self._bins:
                if isinstance(bins_item_data, UnknownType):
                    bins_item = bins_item_data.value
                elif isinstance(bins_item_data, BulkAssemblyFragmentBin):
                    bins_item = bins_item_data.to_dict()

                else:
                    bins_item = bins_item_data.to_dict()

                bins.append(bins_item)

        constructs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._constructs, Unset):
            constructs = self._constructs.to_dict()

        fragments: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._fragments, Unset):
            fragments = []
            for fragments_item_data in self._fragments:
                fragments_item = fragments_item_data.to_dict()

                fragments.append(fragments_item)

        method: Union[Unset, Dict[str, Any]]
        if isinstance(self._method, Unset):
            method = UNSET
        elif isinstance(self._method, UnknownType):
            method = self._method.value
        elif isinstance(self._method, BulkAssemblyGoldenGateMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        elif isinstance(self._method, BulkAssemblyGibsonMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        elif isinstance(self._method, BulkAssemblyHomologyMethod):
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        else:
            method = UNSET
            if not isinstance(self._method, Unset):
                method = self._method.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bins is not UNSET:
            field_dict["bins"] = bins
        if constructs is not UNSET:
            field_dict["constructs"] = constructs
        if fragments is not UNSET:
            field_dict["fragments"] = fragments
        if method is not UNSET:
            field_dict["method"] = method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bins() -> Union[
            Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]
        ]:
            bins = []
            _bins = d.pop("bins")
            for bins_item_data in _bins or []:

                def _parse_bins_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]:
                    bins_item: Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]
                    discriminator_value: str = cast(str, data.get("binType"))
                    if discriminator_value is not None:
                        if discriminator_value == "CONSTANT":
                            bins_item = BulkAssemblyConstantBin.from_dict(data, strict=False)

                            return bins_item
                        if discriminator_value == "FRAGMENT":
                            bins_item = BulkAssemblyFragmentBin.from_dict(data, strict=False)

                            return bins_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = BulkAssemblyFragmentBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        bins_item = BulkAssemblyConstantBin.from_dict(data, strict=True)

                        return bins_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                bins_item = _parse_bins_item(bins_item_data)

                bins.append(bins_item)

            return bins

        try:
            bins = get_bins()
        except KeyError:
            if strict:
                raise
            bins = cast(
                Union[Unset, List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]],
                UNSET,
            )

        def get_constructs() -> Union[Unset, FinalizedBulkAssemblyConstructs]:
            constructs: Union[Unset, Union[Unset, FinalizedBulkAssemblyConstructs]] = UNSET
            _constructs = d.pop("constructs")

            if not isinstance(_constructs, Unset):
                constructs = FinalizedBulkAssemblyConstructs.from_dict(_constructs)

            return constructs

        try:
            constructs = get_constructs()
        except KeyError:
            if strict:
                raise
            constructs = cast(Union[Unset, FinalizedBulkAssemblyConstructs], UNSET)

        def get_fragments() -> Union[Unset, List[BulkAssemblyFragmentShared]]:
            fragments = []
            _fragments = d.pop("fragments")
            for fragments_item_data in _fragments or []:
                fragments_item = BulkAssemblyFragmentShared.from_dict(fragments_item_data, strict=False)

                fragments.append(fragments_item)

            return fragments

        try:
            fragments = get_fragments()
        except KeyError:
            if strict:
                raise
            fragments = cast(Union[Unset, List[BulkAssemblyFragmentShared]], UNSET)

        def get_method() -> Union[
            Unset,
            BulkAssemblyGoldenGateMethod,
            BulkAssemblyGibsonMethod,
            BulkAssemblyHomologyMethod,
            BulkAssemblyConcatenationMethod,
            UnknownType,
        ]:
            method: Union[
                Unset,
                BulkAssemblyGoldenGateMethod,
                BulkAssemblyGibsonMethod,
                BulkAssemblyHomologyMethod,
                BulkAssemblyConcatenationMethod,
                UnknownType,
            ]
            _method = d.pop("method")

            if not isinstance(_method, Unset):
                discriminator = _method["type"]
                if discriminator == "CONCATENATION":
                    method = BulkAssemblyConcatenationMethod.from_dict(_method)
                elif discriminator == "GIBSON":
                    method = BulkAssemblyGibsonMethod.from_dict(_method)
                elif discriminator == "GOLDEN_GATE":
                    method = BulkAssemblyGoldenGateMethod.from_dict(_method)
                elif discriminator == "HOMOLOGY":
                    method = BulkAssemblyHomologyMethod.from_dict(_method)
                else:
                    method = UnknownType(value=_method)

            return method

        try:
            method = get_method()
        except KeyError:
            if strict:
                raise
            method = cast(
                Union[
                    Unset,
                    BulkAssemblyGoldenGateMethod,
                    BulkAssemblyGibsonMethod,
                    BulkAssemblyHomologyMethod,
                    BulkAssemblyConcatenationMethod,
                    UnknownType,
                ],
                UNSET,
            )

        finalized_bulk_assembly = cls(
            bins=bins,
            constructs=constructs,
            fragments=fragments,
            method=method,
        )

        return finalized_bulk_assembly

    @property
    def bins(self) -> List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]:
        if isinstance(self._bins, Unset):
            raise NotPresentError(self, "bins")
        return self._bins

    @bins.setter
    def bins(self, value: List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]) -> None:
        self._bins = value

    @bins.deleter
    def bins(self) -> None:
        self._bins = UNSET

    @property
    def constructs(self) -> FinalizedBulkAssemblyConstructs:
        if isinstance(self._constructs, Unset):
            raise NotPresentError(self, "constructs")
        return self._constructs

    @constructs.setter
    def constructs(self, value: FinalizedBulkAssemblyConstructs) -> None:
        self._constructs = value

    @constructs.deleter
    def constructs(self) -> None:
        self._constructs = UNSET

    @property
    def fragments(self) -> List[BulkAssemblyFragmentShared]:
        if isinstance(self._fragments, Unset):
            raise NotPresentError(self, "fragments")
        return self._fragments

    @fragments.setter
    def fragments(self, value: List[BulkAssemblyFragmentShared]) -> None:
        self._fragments = value

    @fragments.deleter
    def fragments(self) -> None:
        self._fragments = UNSET

    @property
    def method(
        self,
    ) -> Union[
        BulkAssemblyGoldenGateMethod,
        BulkAssemblyGibsonMethod,
        BulkAssemblyHomologyMethod,
        BulkAssemblyConcatenationMethod,
        UnknownType,
    ]:
        if isinstance(self._method, Unset):
            raise NotPresentError(self, "method")
        return self._method

    @method.setter
    def method(
        self,
        value: Union[
            BulkAssemblyGoldenGateMethod,
            BulkAssemblyGibsonMethod,
            BulkAssemblyHomologyMethod,
            BulkAssemblyConcatenationMethod,
            UnknownType,
        ],
    ) -> None:
        self._method = value

    @method.deleter
    def method(self) -> None:
        self._method = UNSET
