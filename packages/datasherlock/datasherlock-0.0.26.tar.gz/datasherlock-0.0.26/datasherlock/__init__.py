from datasherlock.database import DatabaseClient
from datasherlock.request import DatasherlockClient, DatasherlockCloudClient
from tabulate import tabulate
from typing import Any, Dict, Optional, Union


class DataSherlock:
    """
    DataSherlock class for interacting with a database and Datasherlock Cloud.

    Parameters:
        - token (str): Bearer token for Datasherlock Cloud.
        - db_type (str): Type of the database.
        - db_config (Dict[str, Union[str, int]]): Configuration for the database.
    """

    def __init__(
        self, token: str, db_type: str, db_config: Dict[str, Union[str, int]], region: str = "ap-south-1"
    ) -> None:
        """
        Initialize DataSherlock instance.

        Parameters:
            - token (str): Bearer token for Datasherlock Cloud.
            - db_type (str): Type of the database.
            - db_config (Dict[str, Union[str, int]]): Configuration for the database.
        """
        self.db_client: Optional[DatabaseClient] = None
        if db_type and db_config:
            try:
                self.db_client = DatabaseClient(db_type, db_config)
            except Exception as e:
                raise ValueError(f"Error initializing DatabaseClient: {str(e)}")
        self.cloud: DatasherlockCloudClient = DatasherlockCloudClient(
            bearer_token=token,
            region=region
        )
        self.db_config: Dict[str, Union[str, int]] = db_config
        self.db_type: str = db_type

    def ask(
        self,
        question: str = "",
        sql: str = "",
        name: str = "",
        error: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Ask a question to DataSherlock Cloud.

        Parameters:
            - question (str): The question to ask the agent.
            - sql (str): SQL query to execute (optional).
            - name (str): Name of the agent to ask the question (optional).
            - error (Optional[str]): Custom error message (optional).

        Returns:
            Dict[str, Any]: Result of the agent's response or query execution.

        Raises:
            ValueError: If the specified agent name is not found.
        """
        if not name:
            raise ValueError("Please provide a valid agent name.")
        
        try:
            agent = next((x for x in self.cloud.list_agent(registration_data={}).data if x.name == name), None)
            if not agent:
                raise ValueError("Agent not found. Please provide a correct agent name.")
            
            request = {"question": question, "host": self.db_config.get("host", "")}
            query = self.cloud.ask_agent(registration_data=request)
            
            if self.db_client:
                return {"query": query, "data": self.db_client.execute_query(query=query)}
            return {"query": query}
        except Exception as e:
            raise ValueError(f"Error while asking question: {str(e)}")

    def list(self) -> str:
        """
        List agents and print the result in a tabular format.

        Returns:
            str: Tabulated list of agents.
        """
        try:
            result = self.cloud.list_agent(registration_data={}).data
            responses = [
                {"id": data.id, "name": data.name, "url": data.url, "type": data.type, "host": data.host}
                for data in result
            ]
            return tabulate(responses, headers="keys", tablefmt="psql")
        except Exception as e:
            raise ValueError(f"Error while listing agents: {str(e)}")

    def register(self, name: str) -> str:
        """
        Register database metadata agents.

        Parameters:
            - name (str): Name of the agent to register.

        Returns:
            str: Result of registration in a tabulated format.
        """
        if not self.db_client:
            raise ValueError("Please provide database configuration.")

        try:
            data = self.db_client.generate_schema()
            print(self.db_client.get_platform_check())

            schemas = [{"name": key, "data": str(val)} for key, val in data.items()]

            request = {
                "name": name,
                "host": self.db_config.get("host", ""),
                "database": self.db_config["database"],
                "username": self.db_config.get("user", ""),
                "type": self.db_type,
                "tables": [],
                "schema": schemas,
            }

            result = self.cloud.register_agent(registration_data=request)

            return tabulate([{"id": result["agent_id"], "url": result["url"], "token": result["token"]}])
        except Exception as e:
            raise ValueError(f"Error while registering agent: {str(e)}")
    
    def db(self) -> Optional[DatabaseClient]:
        """
        Get the DatabaseClient instance.

        Returns:
            Optional[DatabaseClient]: DatabaseClient instance.
        """
        return self.db_client
