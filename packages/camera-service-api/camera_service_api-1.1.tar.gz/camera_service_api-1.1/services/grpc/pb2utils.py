from datetime import datetime
from typing import Union

import grpc


def value_or_empty(s: Union[str, None]) -> str:
    if s is None:
        return ''
    return s


def value_or_empty_dict(s: dict, name: str) -> str:
    if name in s:
        return value_or_empty(s[name])
    return ''


def value_or_empty_dict_float(s: dict, name: str) -> int:
    if name in s:
        return value_or_zero(s[name])
    return 0


def value_or_empty_dict_datetime(s: dict, name: str) -> float:
    if name in s:
        return from_datetime_to_float(s[name])
    return 0


def value_or_zero(s: Union[int, None], z: int = 0) -> int:
    if s is None:
        return z
    return s


def value_or_float_zero(s: Union[float, None], z: float = 0.) -> float:
    if s is None:
        return z
    return s


def from_float_to_datetime(s: Union[float, None]) -> Union[datetime, None]:
    if s is None:
        return None
    if s < 0:
        return None
    return datetime.fromtimestamp(s)


def from_datetime_to_float(ts: datetime) -> float:
    if ts is None:
        return -1

    return ts.timestamp()


class RemoveError(Exception):
    """Raised by the gRPC library to indicate non-OK-status RPC termination."""

    def __init__(self, e: grpc.RpcError):
        self.code = e.code()
        self.message = e.details()



def wrapper_rpc_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except grpc.RpcError as rpc_error:
            raise RemoveError(rpc_error)

    return wrapper
