# Metals-API Python SDK

[Metals-API](https://metals-api.com) - The ultimate API for accessing precious metals spot prices and historical data effortlessly. Explore real-time and historical metal rates with exceptional accuracy.

## Installation

You can install Metals-API Python SDK with pip.

```bash
pip metals_api_zylalabs
```

## Usage

The Metals-API Python SDK is a wrapper around the [requests](https://docs.python-requests.org/en/master/) library. Metals-API supports a GET request for now.

Sign-up to Metals-API to [get your API key](https://metals-api.com/register) and some credits to get started.

### Making the GET request

```python
>>> from metals_api_zylalabs.main import MetalsAPI

>>> client = MetalsAPI(access_key='REPLACE-WITH-YOUR-ACCESS-KEY')

>>> response = client.get_latest("base", ["symbols"])
```

You can find all the documentation on [Metals documentation](https://metals-api.com/documentation).