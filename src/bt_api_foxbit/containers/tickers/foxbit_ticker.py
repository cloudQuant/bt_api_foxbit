from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData


class FoxbitRequestTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str = "",
        asset_type: str = "SPOT",
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "FOXBIT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_volume: float | None = None
        self.server_time: float | None = None
        self.has_been_init_data = False

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "FoxbitRequestTickerData":
        return cls(data, has_been_json_encoded=True)

    def init_data(self) -> "FoxbitRequestTickerData":
        if not self.has_been_json_encoded:
            self.ticker_data = (
                json.loads(self.ticker_info)
                if isinstance(self.ticker_info, str)
                else self.ticker_info
            )
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = self.ticker_data if isinstance(self.ticker_data, dict) else {}
        ticker_data = data.get("ticker", data) if isinstance(data, dict) else {}
        self.ticker_symbol_name = self.symbol_name or None
        self.last_price = float(ticker_data.get("last", 0.0))
        self.bid_price = float(ticker_data.get("buy", ticker_data.get("bid", 0.0)))
        self.ask_price = float(ticker_data.get("sell", ticker_data.get("ask", 0.0)))
        self.bid_volume = float(ticker_data.get("bid_quantity", 0.0))
        self.ask_volume = float(ticker_data.get("ask_quantity", 0.0))
        self.last_volume = float(ticker_data.get("volume", 0.0))
        self.server_time = float(ticker_data.get("timestamp", 0.0) or 0.0)
        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_ticker_symbol_name(self) -> str | None:
        self.init_data()
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | None:
        self.init_data()
        return self.server_time

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        self.init_data()
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        self.init_data()
        return self.ask_volume

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_last_volume(self) -> float | None:
        self.init_data()
        return self.last_volume
