# bt_api_foxbit

Foxbit exchange adapter for bt_api.

## Installation

```bash
pip install bt_api_foxbit
```

## Usage

```python
from bt_api_foxbit import register_foxbit
register_foxbit()

from bt_api_py import BtApi
api = BtApi(exchange_kwargs={"FOXBIT___SPOT": {"api_key": "...", "secret": "..."}})
ticker = api.get_tick("FOXBIT___SPOT", "BTCBRL")
```
