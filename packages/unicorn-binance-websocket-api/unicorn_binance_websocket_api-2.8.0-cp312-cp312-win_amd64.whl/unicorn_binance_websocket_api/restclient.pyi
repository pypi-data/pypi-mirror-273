import logging
from _typeshed import Incomplete
from typing import Optional, Tuple, Union
from unicorn_binance_rest_api import BinanceRestApiManager

__logger__: logging.getLogger
logger = __logger__

class BinanceWebSocketApiRestclient:
    threading_lock: Incomplete
    debug: Incomplete
    disable_colorama: Incomplete
    exchange: Incomplete
    lucit_api_secret: Incomplete
    lucit_license_ini: Incomplete
    lucit_license_profile: Incomplete
    lucit_license_token: Incomplete
    restful_base_uri: Incomplete
    show_secrets_in_logs: Incomplete
    socks5_proxy_server: Incomplete
    socks5_proxy_user: Incomplete
    socks5_proxy_pass: Incomplete
    socks5_proxy_ssl_verification: Incomplete
    stream_list: Incomplete
    ubra: Incomplete
    warn_on_update: Incomplete
    sigterm: bool
    def __init__(self, debug: Optional[bool] = ..., disable_colorama: Optional[bool] = ..., exchange: Optional[str] = ..., lucit_api_secret: Optional[str] = ..., lucit_license_ini: str = ..., lucit_license_profile: Optional[str] = ..., lucit_license_token: Optional[str] = ..., restful_base_uri: Optional[str] = ..., show_secrets_in_logs: Optional[bool] = ..., socks5_proxy_server: Optional[str] = ..., socks5_proxy_user: Optional[str] = ..., socks5_proxy_pass: Optional[str] = ..., socks5_proxy_ssl_verification: Optional[bool] = ..., stream_list: dict = ..., ubra: BinanceRestApiManager = ..., warn_on_update: Optional[bool] = ...) -> None: ...
    def delete_listen_key(self, stream_id: Incomplete | None = ...) -> Tuple[Union[str, None], Union[dict, None]]: ...
    def get_binance_api_status(self) -> dict: ...
    def get_listen_key(self, stream_id: Incomplete | None = ...) -> Tuple[Union[dict, None], Union[dict, None]]: ...
    def keepalive_listen_key(self, stream_id: Incomplete | None = ...) -> Tuple[Union[str, None], Union[dict, None]]: ...
    def stop(self) -> bool: ...
