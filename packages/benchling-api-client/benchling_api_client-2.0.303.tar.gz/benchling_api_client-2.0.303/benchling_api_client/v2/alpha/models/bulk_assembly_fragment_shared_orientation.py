from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class BulkAssemblyFragmentSharedOrientation(Enums.KnownString):
    FORWARD = "FORWARD"
    REVERSE = "REVERSE"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "BulkAssemblyFragmentSharedOrientation":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of BulkAssemblyFragmentSharedOrientation must be a string (encountered: {val})"
            )
        newcls = Enum("BulkAssemblyFragmentSharedOrientation", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(BulkAssemblyFragmentSharedOrientation, getattr(newcls, "_UNKNOWN"))
