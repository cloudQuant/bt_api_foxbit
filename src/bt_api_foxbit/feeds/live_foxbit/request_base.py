from __future__ import annotations

import hashlib
import hmac
import time
import urllib.parse
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient

from bt_api_foxbit.exchange_data import FoxbitExchangeDataSpot


class FoxbitRequestData(Feed):
    _exchange_data = FoxbitExchangeDataSpot()

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "FOXBIT___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = self._exchange_data
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self.api_secret = (
            kwargs.get("private_key") or kwargs.get("api_secret") or kwargs.get("secret_key") or ""
        )
        self.secret = self.api_secret
        self._params.api_key = self.api_key
        self._params.api_secret = self.api_secret
        self._http_client = HttpClient(
            venue=self.exchange_name, timeout=kwargs.get("timeout", 10.0)
        )

    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str) -> str:
        message = timestamp + method.upper() + request_path + body
        return hmac.new(
            self.secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def _get_headers(
        self,
        method: str,
        request_path: str,
        params: dict[str, Any] | None = None,
        body: str | None = "",
    ) -> dict[str, str]:
        timestamp = str(int(time.time() * 1000))
        encoded_params = ""
        if params:
            encoded_params = urllib.parse.urlencode(params)
        payload = body or encoded_params
        signature = self._generate_signature(timestamp, method, request_path, payload)
        return {
            "X-FB-ACCESS-KEY": self.api_key,
            "X-FB-ACCESS-TIMESTAMP": timestamp,
            "X-FB-ACCESS-SIGNATURE": signature,
            "Content-Type": "application/json",
        }

    def _format_market(self, symbol: str) -> str:
        return symbol.lower()

    def _build_url(self, path: str, params: dict[str, Any] | None = None) -> str:
        base_url = self._exchange_data.get_rest_url().rstrip("/")
        request_path = path if path.startswith("/") else f"/{path}"
        if not params:
            return f"{base_url}{request_path}"
        return f"{base_url}{request_path}?{urllib.parse.urlencode(params)}"

    def request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: float = 10.0,
    ) -> RequestData:
        json_body = body if isinstance(body, dict) else None
        response = self._http_client.request(
            method="GET",
            url=self._build_url(path, params),
            headers=self._get_headers("GET", path, params, body if isinstance(body, str) else ""),
            json_data=json_body,
            timeout=timeout,
        )
        return RequestData(response, extra_data)

    async def async_request(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: float = 10.0,
    ) -> RequestData:
        json_body = body if isinstance(body, dict) else None
        response = await self._http_client.async_request(
            method="GET",
            url=self._build_url(path, params),
            headers=self._get_headers("GET", path, params, body if isinstance(body, str) else ""),
            json_data=json_body,
            timeout=timeout,
        )
        return RequestData(response, extra_data)

    def async_callback(self, future: Any) -> None:
        if self.data_queue is None:
            return
        self.data_queue.put(future.result())

    def connect(self) -> None:
        return None

    def is_connected(self) -> bool:
        return True

    def disconnect(self) -> None:
        super().disconnect()
