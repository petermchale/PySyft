# stdlib
from collections.abc import Callable
from enum import Enum
from typing import Any
from typing import cast

# third party
import docker
from docker.models.containers import Container

# relative
from ...client.api import APIRegistry
from ...serde.serializable import serializable
from ...store.linked_obj import LinkedObject
from ...types.base import SyftBaseModel
from ...types.datetime import DateTime
from ...types.syft_migration import migrate
from ...types.syft_object import SYFT_OBJECT_VERSION_2
from ...types.syft_object import SYFT_OBJECT_VERSION_3
from ...types.syft_object import SyftObject
from ...types.syft_object import short_uid
from ...types.transforms import drop
from ...types.transforms import make_set_default
from ...types.uid import UID
from ...util import options
from ...util.colors import SURFACE
from ...util.notebook_ui.styles import FONT_CSS
from ...util.notebook_ui.styles import ITABLES_CSS
from ..response import SyftError
from .worker_image import SyftWorkerImage


@serializable()
class WorkerStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    STOPPED = "Stopped"
    RESTARTED = "Restarted"


@serializable()
class ConsumerState(Enum):
    IDLE = "Idle"
    CONSUMING = "Consuming"
    DETACHED = "Detached"


@serializable()
class WorkerHealth(Enum):
    HEALTHY = "✅"
    UNHEALTHY = "❌"


@serializable()
class SyftWorkerV2(SyftObject):
    __canonical_name__ = "SyftWorker"
    __version__ = SYFT_OBJECT_VERSION_2

    __attr_unique__ = ["name"]
    __attr_searchable__ = ["name", "container_id"]
    __repr_attrs__ = [
        "name",
        "container_id",
        "image",
        "status",
        "healthcheck",
        "worker_pool_name",
        "created_at",
    ]

    id: UID
    name: str
    container_id: str | None = None
    created_at: DateTime = DateTime.now()
    healthcheck: WorkerHealth | None = None
    status: WorkerStatus
    image: SyftWorkerImage | None = None
    worker_pool_name: str
    consumer_state: ConsumerState = ConsumerState.DETACHED
    job_id: UID | None = None


@serializable()
class SyftWorker(SyftObject):
    __canonical_name__ = "SyftWorker"
    __version__ = SYFT_OBJECT_VERSION_3

    __attr_unique__ = ["name"]
    __attr_searchable__ = ["name", "container_id", "to_be_deleted"]
    __repr_attrs__ = [
        "name",
        "container_id",
        "image",
        "status",
        "healthcheck",
        "worker_pool_name",
        "created_at",
    ]

    id: UID
    name: str
    container_id: str | None = None
    created_at: DateTime = DateTime.now()
    healthcheck: WorkerHealth | None = None
    status: WorkerStatus
    image: SyftWorkerImage | None = None
    worker_pool_name: str
    consumer_state: ConsumerState = ConsumerState.DETACHED
    job_id: UID | None = None
    to_be_deleted: bool = False

    @property
    def logs(self) -> str | SyftError:
        api = APIRegistry.api_for(
            server_uid=self.syft_server_location,
            user_verify_key=self.syft_client_verify_key,
        )
        if api is None:
            return SyftError(message=f"You must login to {self.server_uid}")
        return api.services.worker.logs(uid=self.id)

    def get_job_repr(self) -> str:
        if self.job_id is not None:
            api = APIRegistry.api_for(
                server_uid=self.syft_server_location,
                user_verify_key=self.syft_client_verify_key,
            )
            if api is None:
                return SyftError(message=f"You must login to {self.server_uid}")
            job = api.services.job.get(self.job_id)
            if job.action.user_code_id is not None:
                func_name = api.services.code.get_by_id(
                    job.action.user_code_id
                ).service_func_name
                return f"{func_name} ({short_uid(self.job_id)})"
            else:
                return f"action ({short_uid(self.job_id)})"
        else:
            return ""

    def refresh_status(self) -> SyftError | None:
        api = APIRegistry.api_for(
            server_uid=self.syft_server_location,
            user_verify_key=self.syft_client_verify_key,
        )
        if api is None:
            return SyftError(message=f"You must login to {self.server_uid}")

        res = api.services.worker.status(uid=self.id)
        if isinstance(res, SyftError):
            return res

        self.status, self.healthcheck = res
        return None

    def _coll_repr_(self) -> dict[str, Any]:
        self.refresh_status()

        if self.image and self.image.image_identifier:
            image_name_with_tag = self.image.image_identifier.full_name_with_tag
        else:
            image_name_with_tag = "In Memory Worker"

        healthcheck = self.healthcheck.value if self.healthcheck is not None else ""

        return {
            "Name": self.name,
            "Image": image_name_with_tag,
            "Healthcheck (health / unhealthy)": f"{healthcheck}",
            "Status": f"{self.status.value}",
            "Job": self.get_job_repr(),
            "Created at": str(self.created_at),
            "Container id": self.container_id,
            "Consumer state": str(self.consumer_state.value.lower()),
        }


@serializable()
class WorkerPool(SyftObject):
    __canonical_name__ = "WorkerPool"
    __version__ = SYFT_OBJECT_VERSION_2

    __attr_unique__ = ["name"]
    __attr_searchable__ = ["name", "image_id"]
    __repr_attrs__ = [
        "name",
        "image",
        "max_count",
        "workers",
        "created_at",
    ]
    __table_sort_attr__ = "Created at"

    name: str
    image_id: UID | None = None
    max_count: int
    worker_list: list[LinkedObject]
    created_at: DateTime = DateTime.now()

    @property
    def image(self) -> SyftWorkerImage | SyftError | None:
        """
        Get the pool's image using the worker_image service API. This way we
        get the latest state of the image from the SyftWorkerImageStash
        """
        api = APIRegistry.api_for(
            server_uid=self.syft_server_location,
            user_verify_key=self.syft_client_verify_key,
        )
        if api is not None and api.services is not None:
            return api.services.worker_image.get_by_uid(uid=self.image_id)
        else:
            return None

    @property
    def running_workers(self) -> list[SyftWorker] | SyftError:
        """Query the running workers using an API call to the server"""
        _running_workers = [
            worker for worker in self.workers if worker.status == WorkerStatus.RUNNING
        ]

        return _running_workers

    @property
    def healthy_workers(self) -> list[SyftWorker] | SyftError:
        """
        Query the healthy workers using an API call to the server
        """
        _healthy_workers = [
            worker
            for worker in self.workers
            if worker.healthcheck == WorkerHealth.HEALTHY
        ]

        return _healthy_workers

    def _coll_repr_(self) -> dict[str, Any]:
        if self.image and self.image.image_identifier:
            image_name_with_tag = self.image.image_identifier.full_name_with_tag
        else:
            image_name_with_tag = "In Memory Worker"
        return {
            "Pool Name": self.name,
            "Workers": len(self.workers),
            "Healthy (healthy / all)": f"{len(self.healthy_workers)} / {self.max_count}",
            "Running (running / all)": f"{len(self.running_workers)} / {self.max_count}",
            "Image": image_name_with_tag,
            "Created at": str(self.created_at),
        }

    def _repr_html_(self) -> Any:
        return f"""
            <style>
            {FONT_CSS}
            .syft-dataset {{color: {SURFACE[options.color_theme]};}}
            .syft-dataset h3,
            .syft-dataset p
              {{font-family: 'Open Sans';}}
              {ITABLES_CSS}
            </style>
            <div class='syft-dataset'>
            <h3>{self.name}</h3>
            <p class='paragraph-sm'>
                <strong><span class='pr-8'>Created on: </span></strong>
                {self.created_at}
            </p>
            <p class='paragraph-sm'>
                <strong><span class='pr-8'>Healthy Workers:</span></strong>
                {len(self.healthy_workers)} / {self.max_count}
            </p>
            <p class='paragraph-sm'>
                <strong><span class='pr-8'>Running Workers:</span></strong>
                {len(self.running_workers)} / {self.max_count}
            </p>
            {self.workers._repr_html_()}
            """

    @property
    def workers(self) -> list[SyftWorker]:
        resolved_workers = []
        for worker in self.worker_list:
            resolved_worker = worker.resolve
            if isinstance(resolved_worker, SyftError) or resolved_worker is None:
                continue
            resolved_worker.refresh_status()
            resolved_workers.append(resolved_worker)
        return resolved_workers


@serializable()
class WorkerOrchestrationType(Enum):
    DOCKER = "docker"
    KUBERNETES = "k8s"
    PYTHON = "python"


@serializable()
class ContainerSpawnStatus(SyftBaseModel):
    __repr_attrs__ = ["worker_name", "worker", "error"]

    worker_name: str
    worker: SyftWorker | None = None
    error: str | None = None


def _get_worker_container(
    client: docker.DockerClient,
    worker: SyftWorker,
) -> Container | SyftError:
    try:
        return cast(Container, client.containers.get(worker.container_id))
    except docker.errors.NotFound as e:
        return SyftError(message=f"Worker {worker.id} container not found. Error {e}")
    except docker.errors.APIError as e:
        return SyftError(
            message=f"Unable to access worker {worker.id} container. "
            + f"Container server error {e}"
        )


_CONTAINER_STATUS_TO_WORKER_STATUS: dict[str, WorkerStatus] = dict(
    [
        ("running", WorkerStatus.RUNNING),
        *(
            (status, WorkerStatus.STOPPED)
            for status in ["paused", "removing", "exited", "dead"]
        ),
        ("restarting", WorkerStatus.RESTARTED),
        ("created", WorkerStatus.PENDING),
    ]
)


def _get_worker_container_status(
    client: docker.DockerClient,
    worker: SyftWorker,
    container: Container | None = None,
) -> Container | SyftError:
    if container is None:
        container = _get_worker_container(client, worker)

    if isinstance(container, SyftError):
        return container

    container_status = container.status

    return _CONTAINER_STATUS_TO_WORKER_STATUS.get(
        container_status,
        SyftError(message=f"Unknown container status: {container_status}"),
    )


@migrate(SyftWorkerV2, SyftWorker)
def upgrade_syft_worker() -> list[Callable]:
    return [
        make_set_default("to_be_deleted", False),
    ]


@migrate(SyftWorker, SyftWorkerV2)
def downgrade_syft_worker() -> list[Callable]:
    return [
        drop(["to_be_deleted"]),
    ]
