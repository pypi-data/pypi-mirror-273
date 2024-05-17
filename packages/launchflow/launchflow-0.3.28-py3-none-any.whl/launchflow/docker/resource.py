from typing import Dict, Optional

from launchflow.context import docker_ctx, find_open_port
from launchflow.resource import Resource, T


class DockerResource(Resource[T]):
    def __init__(
        self,
        name: str,
        docker_image: str,
        env_vars: Optional[Dict[str, str]] = None,
        command: Optional[str] = None,
        ports: Optional[Dict[str, int]] = None,
    ):
        super().__init__(name, "docker", {})
        self.docker_image = docker_image
        self.env_vars = env_vars or {}
        self.command = command
        self.ports = ports or {}

    def connection_info(self):
        raise NotImplementedError

    @property
    def resource_type(self):
        return self.__class__.__name__

    def refresh_ports(self) -> None:
        """
        Refresh the allocated ports with new ones.
        """
        for internal_port in self.ports:
            self.ports[internal_port] = find_open_port()

    def connect(self):
        """
        Synchronously connect to the resource by fetching its connection info.
        """
        connection_info = docker_ctx.get_resource_connection_info_sync(
            image_name=self.docker_image,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    async def connect_async(self):
        """
        Asynchronously connect to the resource by fetching its connection info.
        """
        # TODO: Make this async
        connection_info = docker_ctx.get_resource_connection_info_sync(
            image_name=self.docker_image,
            resource_name=self.name,
        )
        return self._connection_type.model_validate(connection_info)

    def create(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
        api_key: Optional[str] = None,
    ):
        """
        Synchronously create the resource.
        """
        del project_name, environment_name, api_key
        return docker_ctx.create_resource_operation_sync(resource=self, replace=replace)

    async def create_async(
        self,
        *,
        project_name: str = None,
        environment_name: str = None,
        replace: bool = False,
        api_key: Optional[str] = None,
    ):
        """
        Asynchronously create the resource.
        """
        del project_name, environment_name, api_key
        # TODO: Make this async
        return docker_ctx.create_resource_operation_sync(resource=self, replace=replace)
