from __future__ import annotations

from bt_api_foxbit.exchange_data import FoxbitExchangeData, FoxbitExchangeDataSpot
from bt_api_foxbit.feeds.live_foxbit.request_base import FoxbitRequestData
from bt_api_foxbit.feeds.live_foxbit.spot import FoxbitRequestDataSpot
from bt_api_foxbit.plugin import plugin_info, register_foxbit

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "FoxbitExchangeData",
    "FoxbitExchangeDataSpot",
    "FoxbitRequestData",
    "FoxbitRequestDataSpot",
    "plugin_info",
    "register_foxbit",
]
