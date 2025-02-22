# stdlib
from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING

# relative
from .serde.serializable import serializable
from .types.uid import UID

if TYPE_CHECKING:
    # relative
    from .service.service import AbstractService


@serializable()
class ServerType(str, Enum):
    DATASITE = "datasite"
    NETWORK = "network"
    ENCLAVE = "enclave"
    GATEWAY = "gateway"

    def __str__(self) -> str:
        # Use values when transforming ServerType to str
        return self.value


@serializable()
class ServerSideType(str, Enum):
    LOW_SIDE = "low"
    HIGH_SIDE = "high"

    def __str__(self) -> str:
        return self.value


class AbstractServer:
    id: UID | None
    name: str | None
    server_type: ServerType | None
    server_side_type: ServerSideType | None
    in_memory_workers: bool

    def get_service(self, path_or_func: str | Callable) -> "AbstractService":
        raise NotImplementedError
