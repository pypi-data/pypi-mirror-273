# Neuralmap API

Neuralmap is designed by Tensor AI to streamline and enhance every aspect of search and recommandation engines.

## Getting started

To get started with the Neuralmap API client, you'll need to sign up for an API key on the Neuralmap platform. Once you have your API key, you can initialize the API client in your application and start making requests to the Neuralmap API.

### Install the API Client
You can install the Neuralmap API client for Python using the following pip command:

```bash
pip install neuralmap-client
```

This command will download and install the Neuralmap API client along with its dependencies from the Python Package Index (PyPI). Once installed, you can start using the API client to interact with the Neuralmap API and process candidate data programmatically.

### Test your installation
To ensure that the installation of the Neuralmap API client for Python was successful, you can perform a simple test to verify its functionality. Here's a basic example of how you can test the installation:

```python
from neuralmap import BaseClient

client = BaseClient(api_key='your_api_key_here')
client.hello()
```

The full and official documentation can be found [here](https://docs.neuralmap.io).