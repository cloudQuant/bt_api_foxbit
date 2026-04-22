from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry


def register_foxbit() -> None:
    from bt_api_foxbit.exchange_data import FoxbitExchangeDataSpot
    from bt_api_foxbit.feeds.live_foxbit.spot import FoxbitRequestDataSpot

    ExchangeRegistry.register_feed("FOXBIT___SPOT", FoxbitRequestDataSpot)
    ExchangeRegistry.register_exchange_data("FOXBIT___SPOT", FoxbitExchangeDataSpot)
    ExchangeRegistry.register_balance_handler("FOXBIT___SPOT", simple_balance_handler)


def plugin_info() -> PluginInfo:
    from bt_api_foxbit import __version__

    return PluginInfo(
        name="Foxbit",
        version=__version__,
        core_requires="bt_api_base",
        supported_exchanges=("FOXBIT___SPOT",),
        supported_asset_types=("SPOT",),
        plugin_module="bt_api_foxbit",
    )
