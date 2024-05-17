import json
import os
from typing import Dict, List, Optional, Union

import grpc

from client.agent.v1 import agent_connect as agent_connect_client
from client.agent.v1 import agent_pb2 as agent_pb2_client
from cloud.agent.v1 import agent_connect as agent_connect
from cloud.agent.v1 import agent_pb2

class DatasherlockClient:
    """
    DatasherlockClient provides a client for interacting with Datasherlock Agent locally.
    """

    def __init__(
        self,
        host: str,
        secret: str = "",
    ):
        """
        Initialize DatasherlockClient.

        Args:
            host (str): Datasherlock Agent host.
            secret (str, optional): Secret for authentication. Defaults to "".
        """
        self.host = host
        self.secret = secret
        self.metadata = {"Token": self.secret}

    def _create_channel(self) -> agent_connect_client.AgentServiceClient:
        """
        Create a gRPC channel for communication.

        Returns:
            agent_connect_client.AgentServiceClient: gRPC client for Datasherlock Agent.
        """
        return agent_connect_client.AgentServiceClient(self.host, headers=self.metadata)

    def ask_agent(
        self, registration_data: Dict[str, Union[str, List[str], bytes, None]]
    ) -> str:
        """
        Ask Datasherlock Agent a question.

        Args:
            registration_data (Dict[str, Union[str, List[str], bytes, None]]): Registration data.

        Returns:
            str: Response from the Datasherlock Agent.
        """
        try:
            client = self._create_channel()
            request = agent_pb2_client.AskAgentRequest(
                question=registration_data["question"]
            )

            response = client.ask(request)
            return response
        except grpc.RpcError as e:
            print(f"Error while asking question: {e.details()}")
            raise

class DatasherlockCloudClient:
    """
    DatasherlockCloudClient provides a client for interacting with Datasherlock Cloud.
    """

    def __init__(
        self,
        bearer_token: str = "",
        region: str = "ap-south-1"
    ):
        """
        Initialize DatasherlockCloudClient.
        Args:
            host (str, optional): Datasherlock Cloud host. Defaults to "https://api.ap-south-1.datasherlock.io".
            bearer_token (str, optional): Bearer token for authentication. Defaults to "".
        """
        self.region = region
        self.host = os.environ.get("DS_HOST_URL") or f"https://api.{region}.datasherlock.io"
        self.bearer_token = bearer_token
        self.metadata = {"Authorization": "bearer " + self.bearer_token}

    def _create_channel(self) -> agent_connect.AgentServiceClient:
        """
        Create a gRPC channel for communication.

        Returns:
            agent_connect.AgentServiceClient: gRPC client for Datasherlock Cloud.
        """
        return agent_connect.AgentServiceClient(self.host, headers=self.metadata)

    def _handle_grpc_error(self, e: grpc.RpcError):
        print(f"Error during gRPC operation: {e.details()}")
        raise

    def ask_agent(
        self, registration_data: Dict[str, Union[str, List[str], bytes, None]]
    ) -> str:
        """
        Ask Datasherlock Agent in the cloud a question.

        Args:
            registration_data (Dict[str, Union[str, List[str], bytes, None]]): Registration data.

        Returns:
            str: Response from Datasherlock Agent in the cloud.
        """
        try:
            client = self._create_channel()
            request = agent_pb2.AskAgentRequest(question=registration_data["question"], host=registration_data["host"])

            response = client.ask(request)
            return response
        except grpc.RpcError as e:
            self._handle_grpc_error(e)

    def list_agent(
        self, registration_data: Dict[str, Union[str, List[str], bytes, None]]
    ) -> str:
        """
        List available agents in the cloud.

        Args:
            registration_data (Dict[str, Union[str, List[str], bytes, None]]): Registration data.

        Returns:
            str: Response listing available agents.
        """
        try:
            client = self._create_channel()
            request = agent_pb2.ListAgentRequest()
            response = client.list(request)
            return response
        except grpc.RpcError as e:
            self._handle_grpc_error(e)

    def register_agent(
        self, registration_data: Dict[str, Union[str, List[str], bytes, None]]
    ) -> Dict[str, Union[int, str]]:
        """
        Register a new agent in the cloud.

        Args:
            registration_data (Dict[str, Union[str, List[str], bytes, None]]): Registration data.

        Returns:
            Dict[str, Union[int, str]]: Registration result.
        """
        try:
            client = self._create_channel()
            request = agent_pb2.RegisterAgentRequest(
                name=registration_data["name"],
                host=registration_data["host"],
                database=registration_data["database"],
                username=registration_data["username"],
                type=registration_data["type"],
                tables=registration_data["tables"],
                schema=json.dumps(registration_data["schema"]).encode("utf-8"),
            )

            if "target" in registration_data:
                request.target = registration_data["target"]

            response = client.register(request)
            if response.agent_id > 0:
                return {
                    "agent_id": response.agent_id,
                    "token": response.token,
                    "url": response.url,
                }
            else:
                return {"error": "Failed to register agent", "response": response}
        except grpc.RpcError as e:
            self._handle_grpc_error(e)
