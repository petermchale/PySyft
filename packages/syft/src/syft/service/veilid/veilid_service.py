# stdlib
from typing import Callable
from typing import Union

# third party
import requests

# relative
from ...serde.serializable import serializable
from ...store.document_store import DocumentStore
from ...util.telemetry import instrument
from ..context import AuthedServiceContext
from ..network.routes import VeilidNodeRoute
from ..response import SyftError
from ..response import SyftSuccess
from ..service import AbstractService
from ..service import service_method
from ..user.user_roles import DATA_OWNER_ROLE_LEVEL
from .veilid_endpoints import GEN_DHT_KEY_ENDPOINT
from .veilid_endpoints import HEALTHCHECK_ENDPOINT
from .veilid_endpoints import RET_DHT_KEY_ENDPOINT
from .veilid_endpoints import VEILID_SERVICE_URL


@instrument
@serializable()
class VeilidService(AbstractService):
    store: DocumentStore

    def __init__(self, store: DocumentStore) -> None:
        self.store = store

    def perform_request(
        self, method: Callable, endpoint: str, raw: bool = False
    ) -> Union[SyftSuccess, SyftError, str]:
        try:
            response = method(f"{VEILID_SERVICE_URL}{endpoint}")
            response.raise_for_status()
            message = response.json().get("message")
            return message if raw else SyftSuccess(message=message)
        except requests.HTTPError:
            return SyftError(message=f"{response.json()['detail']}")
        except requests.RequestException as e:
            return SyftError(message=f"Failed to perform request. {e}")

    def is_veilid_service_healthy(self) -> bool:
        res = self.perform_request(
            method=requests.get, endpoint=HEALTHCHECK_ENDPOINT, raw=True
        )
        return res == "OK"

    @service_method(
        path="veilid.generate_dht_key",
        name="generate_dht_key",
        roles=DATA_OWNER_ROLE_LEVEL,
    )
    def generate_dht_key(self, context: AuthedServiceContext) -> Union[str, SyftError]:
        if not self.is_veilid_service_healthy():
            return SyftError(
                message="Veilid service is not healthy. Please try again later."
            )
        return self.perform_request(
            method=requests.post,
            endpoint=GEN_DHT_KEY_ENDPOINT,
        )

    @service_method(
        path="veilid.retrieve_dht_key",
        name="retrieve_dht_key",
        roles=DATA_OWNER_ROLE_LEVEL,
    )
    def retrieve_dht_key(self, context: AuthedServiceContext) -> Union[str, SyftError]:
        if not self.is_veilid_service_healthy():
            return SyftError(
                message="Veilid service is not healthy. Please try again later."
            )
        return self.perform_request(
            method=requests.get,
            endpoint=RET_DHT_KEY_ENDPOINT,
            raw=True,
        )

    @service_method(
        path="veilid.get_veilid_route",
        name="get_veilid_route",
    )
    def get_veilid_route(
        self, context: AuthedServiceContext
    ) -> Union[VeilidNodeRoute, SyftError]:
        dht_key = self.retrieve_dht_key(context)
        if isinstance(dht_key, SyftError):
            return dht_key
        return VeilidNodeRoute(dht_key=dht_key)
