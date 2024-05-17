# Sherlock

## Introduction
The Datasherlock Python SDK allows you to seamlessly integrate Datasherlock's powerful database querying capabilities into your Python applications. With this SDK, you can interact with Datasherlock's cloud-based service to register your database, ask queries, and retrieve valuable insights without the need for complex SQL queries.

This documentation will guide you through the installation process, usage of the SDK, and provide examples to help you get started.

## Installation

You can install the Datasherlock Python SDK using pip:

```bash
pip install datasherlock
```

## Quick Start

Before using the Datasherlock Python SDK, ensure that you have already registered your agent with the Datasherlock cloud. If you haven't done so, please refer to the Datasherlock platform documentation on agent registration.

Once your agent is registered, you can start using the Python SDK as follows:

```python
from datasherlock import DataSherlock

# Initialize the DataSherlock SDK with api token and database configuration
sherlock = DataSherlock(token="YOUR_API_TOKEN", db_type="mysql", db_config={
    'host': "localhost",
    'database': "employees",
    'user': "root",
    'port': 3306,
    'password': "college",
    'ssl_disabled': True
})

# Register your database with Datasherlock
registration_result = sherlock.register("employees")
print(registration_result)

# Ask a query to retrieve insights, Ask will return you pandas dataframe 
query_result = sherlock.ask("List of department")
print(query_result)

```

### DataSherlock Class

- `token`: Your API access token obtained during registration.
- `db_type`: The type of the database you're using (e.g., "mysql").
- `region`: Datasherlock region.
- `db_config`: A dictionary containing your database configuration, including host, database name, user, port, password, and SSL settings.

### SDK Methods

- `register(database_name)`: Registers your database with Datasherlock.
- `ask(query)`: Submits a query to Datasherlock and retrieves the result.
- `list()`: Retrieves a list of available queries from Datasherlock.
- `db()`: Retrieves a db client.
