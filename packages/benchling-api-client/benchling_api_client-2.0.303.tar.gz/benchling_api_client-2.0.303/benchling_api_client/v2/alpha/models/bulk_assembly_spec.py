from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.bulk_assembly_concatenation_method import BulkAssemblyConcatenationMethod
from ..models.bulk_assembly_constant_bin import BulkAssemblyConstantBin
from ..models.bulk_assembly_fragment_bin import BulkAssemblyFragmentBin
from ..models.bulk_assembly_gibson_method import BulkAssemblyGibsonMethod
from ..models.bulk_assembly_golden_gate_method import BulkAssemblyGoldenGateMethod
from ..models.bulk_assembly_homology_method import BulkAssemblyHomologyMethod
from ..models.bulk_assembly_spec_fragments_item import BulkAssemblySpecFragmentsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkAssemblySpec")


@attr.s(auto_attribs=True, repr=False)
class BulkAssemblySpec:
    """  """

    _assembly_parameters: Union[
        BulkAssemblyGoldenGateMethod,
        BulkAssemblyGibsonMethod,
        BulkAssemblyHomologyMethod,
        BulkAssemblyConcatenationMethod,
        UnknownType,
    ]
    _bins: List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]
    _constructs: List[str]
    _folder_id: str
    _fragments: List[BulkAssemblySpecFragmentsItem]
    _name: str

    def __repr__(self):
        fields = []
        fields.append("assembly_parameters={}".format(repr(self._assembly_parameters)))
        fields.append("bins={}".format(repr(self._bins)))
        fields.append("constructs={}".format(repr(self._constructs)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("fragments={}".format(repr(self._fragments)))
        fields.append("name={}".format(repr(self._name)))
        return "BulkAssemblySpec({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self._assembly_parameters, UnknownType):
            assembly_parameters = self._assembly_parameters.value
        elif isinstance(self._assembly_parameters, BulkAssemblyGoldenGateMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        elif isinstance(self._assembly_parameters, BulkAssemblyGibsonMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        elif isinstance(self._assembly_parameters, BulkAssemblyHomologyMethod):
            assembly_parameters = self._assembly_parameters.to_dict()

        else:
            assembly_parameters = self._assembly_parameters.to_dict()

        bins = []
        for bins_item_data in self._bins:
            if isinstance(bins_item_data, UnknownType):
                bins_item = bins_item_data.value
            elif isinstance(bins_item_data, BulkAssemblyFragmentBin):
                bins_item = bins_item_data.to_dict()

            else:
                bins_item = bins_item_data.to_dict()

            bins.append(bins_item)

        constructs = self._constructs

        folder_id = self._folder_id
        fragments = []
        for fragments_item_data in self._fragments:
            fragments_item = fragments_item_data.to_dict()

            fragments.append(fragments_item)

        name = self._name

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if assembly_parameters is not UNSET:
            field_dict["assemblyParameters"] = assembly_parameters
        if bins is not UNSET:
            field_dict["bins"] = bins
        if constructs is not UNSET:
            field_dict["constructs"] = constructs
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if fragments is not UNSET:
            field_dict["fragments"] = fragments
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_assembly_parameters() -> Union[
            BulkAssemblyGoldenGateMethod,
            BulkAssemblyGibsonMethod,
            BulkAssemblyHomologyMethod,
            BulkAssemblyConcatenationMethod,
            UnknownType,
        ]:
            assembly_parameters: Union[
                BulkAssemblyGoldenGateMethod,
                BulkAssemblyGibsonMethod,
                BulkAssemblyHomologyMethod,
                BulkAssemblyConcatenationMethod,
                UnknownType,
            ]
            _assembly_parameters = d.pop("assemblyParameters")

            if True:
                discriminator = _assembly_parameters["type"]
                if discriminator == "CONCATENATION":
                    assembly_parameters = BulkAssemblyConcatenationMethod.from_dict(_assembly_parameters)
                elif discriminator == "GIBSON":
                    assembly_parameters = BulkAssemblyGibsonMethod.from_dict(_assembly_parameters)
                elif discriminator == "GOLDEN_GATE":
                    assembly_parameters = BulkAssemblyGoldenGateMethod.from_dict(_assembly_parameters)
                elif discriminator == "HOMOLOGY":
                    assembly_parameters = BulkAssemblyHomologyMethod.from_dict(_assembly_parameters)
                else:
                    assembly_parameters = UnknownType(value=_assembly_parameters)

            return assembly_parameters

        try:
            assembly_parameters = get_assembly_parameters()
        except KeyError:
            if strict:
                raise
            assembly_parameters = cast(
                Union[
                    BulkAssemblyGoldenGateMethod,
                    BulkAssemblyGibsonMethod,
                    BulkAssemblyHomologyMethod,
                    BulkAssemblyConcatenationMethod,
                    UnknownType,
                ],
                UNSET,
            )

        def get_bins() -> List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]:
            bins = []
            _bins = d.pop("bins")
            for bins_item_data in _bins:

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
            bins = cast(List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]], UNSET)

        def get_constructs() -> List[str]:
            constructs = cast(List[str], d.pop("constructs"))

            return constructs

        try:
            constructs = get_constructs()
        except KeyError:
            if strict:
                raise
            constructs = cast(List[str], UNSET)

        def get_folder_id() -> str:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(str, UNSET)

        def get_fragments() -> List[BulkAssemblySpecFragmentsItem]:
            fragments = []
            _fragments = d.pop("fragments")
            for fragments_item_data in _fragments:
                fragments_item = BulkAssemblySpecFragmentsItem.from_dict(fragments_item_data, strict=False)

                fragments.append(fragments_item)

            return fragments

        try:
            fragments = get_fragments()
        except KeyError:
            if strict:
                raise
            fragments = cast(List[BulkAssemblySpecFragmentsItem], UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        bulk_assembly_spec = cls(
            assembly_parameters=assembly_parameters,
            bins=bins,
            constructs=constructs,
            folder_id=folder_id,
            fragments=fragments,
            name=name,
        )

        return bulk_assembly_spec

    @property
    def assembly_parameters(
        self,
    ) -> Union[
        BulkAssemblyGoldenGateMethod,
        BulkAssemblyGibsonMethod,
        BulkAssemblyHomologyMethod,
        BulkAssemblyConcatenationMethod,
        UnknownType,
    ]:
        """ Assembly-wide parameters. """
        if isinstance(self._assembly_parameters, Unset):
            raise NotPresentError(self, "assembly_parameters")
        return self._assembly_parameters

    @assembly_parameters.setter
    def assembly_parameters(
        self,
        value: Union[
            BulkAssemblyGoldenGateMethod,
            BulkAssemblyGibsonMethod,
            BulkAssemblyHomologyMethod,
            BulkAssemblyConcatenationMethod,
            UnknownType,
        ],
    ) -> None:
        self._assembly_parameters = value

    @property
    def bins(self) -> List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]:
        """ Bins are used to group fragments according to their position in the output construct. """
        if isinstance(self._bins, Unset):
            raise NotPresentError(self, "bins")
        return self._bins

    @bins.setter
    def bins(self, value: List[Union[BulkAssemblyFragmentBin, BulkAssemblyConstantBin, UnknownType]]) -> None:
        self._bins = value

    @property
    def constructs(self) -> List[str]:
        """ Ordered list of fragment IDs to use in creating the construct, or a special option (SKIP) to indicate a bin should be skipped. """
        if isinstance(self._constructs, Unset):
            raise NotPresentError(self, "constructs")
        return self._constructs

    @constructs.setter
    def constructs(self, value: List[str]) -> None:
        self._constructs = value

    @property
    def folder_id(self) -> str:
        """ API identifier of the folder in which the assembly should be created. """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @property
    def fragments(self) -> List[BulkAssemblySpecFragmentsItem]:
        """ Fragments to be used in the assembly. """
        if isinstance(self._fragments, Unset):
            raise NotPresentError(self, "fragments")
        return self._fragments

    @fragments.setter
    def fragments(self, value: List[BulkAssemblySpecFragmentsItem]) -> None:
        self._fragments = value

    @property
    def name(self) -> str:
        """ Name of the bulk assembly. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
