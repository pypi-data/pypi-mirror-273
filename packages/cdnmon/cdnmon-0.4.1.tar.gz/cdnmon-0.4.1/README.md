## Introduction

This project provides IP range data of multiple CDN vendors via a Python package named `cdnmon`.

## Installation

```
pip install -i https://pypi.org/simple/ cdnmon
```

## Usage

### List all supported CDNs

```python
from cdnmon import Endpoint

endpoint = Endpoint(access_token="")
cdns = endpoint.list_cdns()
```

### Get a CDN by name

```python
from cdnmon import Endpoint

endpoint = Endpoint(access_token="")
cdn = endpoint.get_cdn(name="cloudflare")
print(cdn)
```

### Get the IP ranges of a specific CDN

```python
from cdnmon import Endpoint

endpoint = Endpoint(access_token="")
cdn = endpoint.get_cdn(name="cloudflare")
latest_ipv4_networks = cdn["ipv4_networks"][-1]
print("Updated at:", latest_ipv4_networks["updated_at"])
print("Source:", latest_ipv4_networks["source"])
print("Networks:")
for latest_ipv4_network in latest_ipv4_networks["networks"]:
    print(latest_ipv4_network)
```

## TODO

- [ ] Support downloading ingress / egress nodes list
- [ ] Add type annotations

## FAQ

### How to obtain an access token?

Please contact <wangyihanger@gmail.com>.
