from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class FoxbitExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "foxbit"


class FoxbitExchangeDataSpot(FoxbitExchangeData):
    _REST_URL = "https://api.foxbit.com.br"
    _WSS_URL = "wss://ws.foxbit.com.br"
    _KLINE_PERIODS = {
        "1m": "60",
        "5m": "300",
        "15m": "900",
        "30m": "1800",
        "1h": "3600",
        "2h": "7200",
        "4h": "14400",
        "6h": "21600",
        "12h": "43200",
        "1d": "86400",
        "1w": "604800",
    }
    _REST_PATHS = {
        "ticker": "/api/v2/markets/{symbol}/ticker",
        "orderbook": "/api/v2/markets/{symbol}/orderbook",
        "trades": "/api/v2/markets/{symbol}/trades",
        "kline": "/api/v2/markets/{symbol}/candles",
        "markets": "/api/v2/markets",
        "balance": "/api/2/balance",
    }

    def __init__(self) -> None:
        super().__init__()
        self.rest_url = self._REST_URL
        self.wss_url = self._WSS_URL
        self.kline_periods = dict(self._KLINE_PERIODS)
        self.rest_paths = dict(self._REST_PATHS)

    def get_rest_url(self) -> str:
        return self.rest_url

    def get_wss_url(self) -> str:
        return self.wss_url

    def get_kline_periods(self) -> dict[str, str]:
        return dict(self.kline_periods)

    def get_symbol(self, symbol: str) -> str:
        return symbol.lower()

    def get_rest_path(self, action: str) -> str:
        return self.rest_paths.get(action, "")

    def get_wss_path(self, action: str) -> str:
        return ""

    def get_local_symbol(self, symbol: str) -> str:
        return symbol.upper()

    def is_trading_enabled(self) -> bool:
        return True
