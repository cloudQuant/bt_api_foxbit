from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorTranslator


class FoxbitErrorTranslator(ErrorTranslator):
    @staticmethod
    def is_error(response: dict[str, Any]) -> bool:
        if not isinstance(response, dict):
            return False
        return response.get("error") is not None or bool(response.get("code", 0) < 0)
