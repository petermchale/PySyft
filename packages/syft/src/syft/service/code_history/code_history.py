# stdlib
from collections.abc import Callable
import json
from typing import Any

# relative
from ...client.api import APIRegistry
from ...client.enclave_client import EnclaveMetadata
from ...serde.serializable import serializable
from ...service.user.user_roles import ServiceRole
from ...types.syft_migration import migrate
from ...types.syft_object import SYFT_OBJECT_VERSION_2
from ...types.syft_object import SYFT_OBJECT_VERSION_3
from ...types.syft_object import SyftObject
from ...types.syft_object import SyftVerifyKey
from ...types.transforms import drop
from ...types.transforms import make_set_default
from ...types.uid import UID
from ...util.notebook_ui.components.tabulator_template import (
    build_tabulator_table_with_data,
)
from ...util.table import prepare_table_data
from ..code.user_code import UserCode
from ..response import SyftError


@serializable()
class CodeHistoryV2(SyftObject):
    # version
    __canonical_name__ = "CodeHistory"
    __version__ = SYFT_OBJECT_VERSION_2

    id: UID
    server_uid: UID
    user_verify_key: SyftVerifyKey
    enclave_metadata: EnclaveMetadata | None = None
    user_code_history: list[UID] = []
    service_func_name: str
    comment_history: list[str] = []


@serializable()
class CodeHistory(SyftObject):
    # version
    __canonical_name__ = "CodeHistory"
    __version__ = SYFT_OBJECT_VERSION_3

    id: UID
    server_uid: UID
    user_verify_key: SyftVerifyKey
    user_code_history: list[UID] = []
    service_func_name: str
    comment_history: list[str] = []

    __attr_searchable__ = ["user_verify_key", "service_func_name"]

    def add_code(self, code: UserCode, comment: str | None = None) -> None:
        self.user_code_history.append(code.id)
        if comment is None:
            comment = ""
        self.comment_history.append(comment)


@serializable()
class CodeHistoryView(SyftObject):
    # version
    __canonical_name__ = "CodeHistoryView"
    __version__ = SYFT_OBJECT_VERSION_2

    id: UID
    user_code_history: list[UserCode] = []
    service_func_name: str
    comment_history: list[str] = []

    def _coll_repr_(self) -> dict[str, int]:
        return {"Number of versions": len(self.user_code_history)}

    def _repr_html_(self) -> str | None:
        rows, metadata = prepare_table_data(self.user_code_history)

        for i, r in enumerate(rows):
            r["Version"] = f"v{i}"
            raw_code = self.user_code_history[i].raw_code
            n_code_lines = raw_code.count("\n")
            if n_code_lines > 5:
                raw_code = "\n".join(raw_code.split("\n", 5))
            r["Code"] = raw_code

        metadata["name"] = "Code History"
        metadata["columns"] += ["Version", "Code"]

        return build_tabulator_table_with_data(rows, metadata)

    def __getitem__(self, index: int | str) -> UserCode | SyftError:
        if isinstance(index, str):
            raise TypeError(f"index {index} must be an integer, not a string")
        api = APIRegistry.api_for(
            self.syft_server_location, self.syft_client_verify_key
        )
        if api is None:
            return SyftError(
                message=f"Can't access the api. You must login to {self.server_uid}"
            )
        if (
            api.user.get_current_user().role.value >= ServiceRole.DATA_OWNER.value
            and index < 0
        ):
            # negative index would dynamically resolve to a different version
            return SyftError(
                message="For security concerns we do not allow negative indexing. \
                Try using absolute values when indexing"
            )
        return self.user_code_history[index]


@serializable()
class CodeHistoriesDict(SyftObject):
    # version
    __canonical_name__ = "CodeHistoriesDict"
    __version__ = SYFT_OBJECT_VERSION_2

    id: UID
    code_versions: dict[str, CodeHistoryView] = {}

    def _repr_html_(self) -> str:
        return f"""
            {self.code_versions._repr_html_()}
            """

    def add_func(self, versions: CodeHistoryView) -> Any:
        self.code_versions[versions.service_func_name] = versions

    def __getitem__(self, name: str | int) -> Any:
        if isinstance(name, int):
            raise TypeError("name argument ({name}) must be a string, not an integer.")
        return self.code_versions[name]

    def __getattr__(self, name: str) -> Any:
        code_versions = object.__getattribute__(self, "code_versions")
        if name in code_versions.keys():
            return code_versions[name]
        return object.__getattribute__(self, name)


@serializable()
class UsersCodeHistoriesDict(SyftObject):
    # version
    __canonical_name__ = "UsersCodeHistoriesDict"
    __version__ = SYFT_OBJECT_VERSION_2

    id: UID
    server_uid: UID
    user_dict: dict[str, list[str]] = {}

    __repr_attrs__ = ["available_keys"]

    @property
    def available_keys(self) -> str:
        return json.dumps(self.user_dict, sort_keys=True, indent=4)

    def __getitem__(self, key: str | int) -> CodeHistoriesDict | SyftError:
        api = APIRegistry.api_for(self.server_uid, self.syft_client_verify_key)
        if api is None:
            return SyftError(
                message=f"Can't access the api. You must login to {self.server_uid}"
            )
        return api.services.code_history.get_history_for_user(key)

    def _repr_html_(self) -> str | None:
        rows = [
            {"User": user, "UserCodes": ", ".join(funcs)}
            for user, funcs in self.user_dict.items()
        ]
        metadata = {
            "name": "UserCode Histories",
            "columns": ["User", "UserCodes"],
            "icon": None,
        }
        return build_tabulator_table_with_data(rows, metadata)


@migrate(CodeHistoryV2, CodeHistory)
def code_history_v2_to_v3() -> list[Callable]:
    return [drop("enclave_metadata")]


@migrate(CodeHistory, CodeHistoryV2)
def code_history_v3_to_v2() -> list[Callable]:
    return [
        make_set_default("enclave_metadata", None),
    ]
