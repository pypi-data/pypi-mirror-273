# Python SDK for statsnet.co
## Installation

```sh
pip install statsnet-python-sdk
```

Requirements:

-   Python 3.8+
-   [httpx](https://pypi.org/project/httpx/)

## Usage
Import statsnet client and set API keys:

```python
from statsnet_python_sdk import Client

token = "123" # or set via STATSNET_API_KEY environment variable
```

```python
client = Client(token)
```

```python
# Get info about current user (/api/v2/user/me)
me = client.me()
```

```python
# Find company by query and jurisdiction (/api/v2/business/search)
companies = client.search(query="казпочта", jurisdiction="kz", limit=5)
# Or without specifiying jurisdiction
companies = client.search(query="казпочта", limit=5)
```

```python
# Get company by id and jurisdiction (/api/v2/business/{jurisdiction}/{id}/paid
company = client.get_company("kz", 1)
```

```python
# Get company meta by id (/api/v2/business/{id}/data/view/meta)
meta = client.get_company_meta(1)
```

```python
# Get company court cases (/business/{id}/court_cases)
court_cases = client.get_company_court_cases(id=1, limit=5)
```

```python
# Get company departments (/business/{id}/department)
departments = client.get_company_departments(id=1, limit=5)
```

```python
# Get company gov contracts (/business/{id}/gov_contracts)
gov_contracts = client.get_company_gov_contracts(id=1, limit=5)
```

```python
# Get company events (/business/{id}/events)
company_events = client.get_company_events(id=1, limit=5)
```

```python
# Get company relations (/business/{id}/relations/table)
company_relations = client.get_company_relations(id=1, limit=5)
```

```python
# Get company by identifier
company = client.get_company_by_identifier("1")
```

##### Limit must be between 1 and 500, 501 is already invalid value