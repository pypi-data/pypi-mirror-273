# Pymerc

> A Python library for interacting with the [Mercatorio] browser based game

## Usage

You must first [generate API credentials](https://play.mercatorio.io/settings/api).
Once generated, you can instantiate a `Client` instance using the credentials.

```python
from pymerc.client import Client

# Create a new client
client = Client(os.environ["API_USER"], os.environ["API_TOKEN"])

# Interact with the various API endpoints
towns = await client.towns.all()
for town in towns:
    print(town.name)
```

## Testing

Since this library parses live API endpoints, mocking values makes little sense.
Instead, you must provide a `.env` file with your API credentials:

```text
API_USER="<USER>"
API_TOKEN="<TOKEN>"
```

The tests will utilize this to validate that all endpoints are parsing correctly:

```shell
pytest .
```

Additionally, you can create an instance of the client to test with using `ipython`:

```shell
> ipython
In [1]: from shell import main
In [2]: await main()
In [3]: from shell import client
In [4]: # Use the client as needed
```

[Mercatorio]: https://mercatorio.io