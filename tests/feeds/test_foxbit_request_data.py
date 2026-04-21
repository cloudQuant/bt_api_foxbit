from unittest.mock import MagicMock
from bt_api_foxbit.feeds.live_foxbit.request_base import FoxbitRequestData
def test_foxbit_disconnect_closes_http_client() -> None:
    request_data = FoxbitRequestData()
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()
