import base64
import binascii
import functools
import hashlib
import hmac
import inspect
import json
import os
import random
import socket
import time
import typing_extensions as typing
import uuid
import warnings

import httpx
import python_socks.sync

from .types import ProxiesType

__all__ = (
    'active_time',
    'decode_sid',
    'deprecated',
    'generateDevice',
    'generateSig',
    'generateTransactionId',
    'generateUserAgent',
    'get_file_type',
    'sid_created_time',
    'sid_to_client_type',
    'sid_to_ip_address',
    'sid_to_uid',
    'updateDevice',
    'uuidString'
)

# intern typing util
P = typing.ParamSpec('P')
R = typing.TypeVar('R')
G = typing.TypeVar('G')
S = typing.TypeVar('S')
T = typing.TypeVar('T')

# constants
PREFIX: typing.Final[str] = '19'
SIGKEY: typing.Final[str] = 'dfa5ed192dda6e88a12fe12130dc6206b1251e44'
DEVKEY: typing.Final[str] = 'e7309ecc0953c6fa60005b2765f99dbbc965c8e9'
NO_ICON_URL = "https://wa1.aminoapps.com/static/img/user-icon-placeholder.png"

def api(path: str) -> str:
    return "https://service.aminoapps.com/api/v1/" + path.removeprefix('/')


def webApi(path: str) -> str:
    return "https://aminoapps.com/api/" + path.removeprefix('/')


def generateSig(data: typing.Union[bytes, str]) -> str:
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(
        bytes.fromhex(PREFIX) + hmac.new(
            bytes.fromhex(SIGKEY),
            data,
            hashlib.sha1
        ).digest()
    ).decode()


def generateDevice(id: typing.Optional[bytes] = None) -> str:
    info = bytes.fromhex(PREFIX) + (id or os.urandom(20))
    device = info + hmac.new(bytes.fromhex(DEVKEY), info, hashlib.sha1).digest()
    return device.hex().upper()


def updateDevice(device: str) -> str:
    return generateDevice(bytes.fromhex(device)[1:21])


def generateUserAgent() -> str:
    return f"Apple iPhone{random.randint(1,99999)},1 iOS v16.5 Main/3.19.0"


def generateTransactionId() -> str:
    return str(uuid.UUID(binascii.hexlify(os.urandom(16)).decode("ascii")))


def uuidString() -> str:
    return str(uuid.uuid4())


def active_time(*, seconds: int = 0, minutes: int = 0, hours: int = 0) -> typing.List[typing.Dict[typing.Literal["start", "end"], int]]:
    total = seconds + minutes * 60 + hours * 60 * 60
    result: typing.List[typing.Dict[typing.Literal["start", "end"], int]] = []
    for _ in range(total // 300):
        result.append({
            'start': int(time.time()),
            'end': int(time.time() + 300)
        })
    if total % 300:
        result.append({
            'start': int(time.time()),
            'end': int(time.time() + total % 300)
        })
    return result


def decode_sid(sid: str) -> typing.Dict[str, typing.Any]:
    """Decode an amino session ID string.

    Parameters
    ----------
    sid : str
        The sid string to decode.

    Returns
    -------
    dict
        The decoded data.

    """
    return json.loads(base64.urlsafe_b64decode(sid + "=" * (4 - len(sid) % 4))[1:-20])


def sid_to_uid(sid: str) -> str:
    """Convert an amino session ID to user ID.

    Parameters
    ----------
    sid : str
        The sid string to convert.

    Returns
    -------
    str
        The user ID.

    """
    return decode_sid(sid)["2"]


def sid_to_ip_address(sid: str) -> str:
    """Convert an amino session ID to IP address.

    Parameters
    ----------
    sid : str
        The sid string to convert.

    Returns
    -------
    str
        The IP address string.

    """
    return decode_sid(sid)["4"]


def sid_created_time(sid: str) -> str:
    """Convert an amino session ID to created-time (datetime).

    Parameters
    ----------
    sid : str
        The sid string to convert.

    Returns
    -------
    str
        The sid created time (datetime)

    """
    return decode_sid(sid)["5"]


def sid_to_client_type(sid: str) -> int:
    """Convert an amino session ID to session client type.

    Parameters
    ----------
    sid : str
        The sid string to convert.

    Returns
    -------
    int
        The client type.

    """
    return decode_sid(sid)["6"]


def get_file_type(name: str, default: str = "jpg") -> str:
    """Get the file type from the given file name.

    Parameters
    ----------
    name : str
        The file name.
    default : str, optional
        The file type to return. Default is 'jpg'.

    Returns
    -------
    str
        The file type.

    """
    try:
        return name[::-1][:name[::-1].index('.')][::-1]
    except (ValueError, IndexError):
        return default


def deprecated(instead: typing.Optional[str] = None) -> typing.Callable[[typing.Callable[P, R]], typing.Callable[P, R]]:
    """Set deprecated functions without altering operation by decoration.

    Parameters
    ----------
    instead: str, optional
        The function instead name.

    Returns
    -------
    Callable
        The decorator function

    """
    def decorator(func: typing.Callable[P, R]) -> typing.Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter
            if instead:
                fmt = "{0.__name__} is deprecated, use {1} instead."
            else:
                fmt = '{0.__name__} is deprecated.'
            warnings.warn(fmt.format(func, instead), stacklevel=3, category=DeprecationWarning)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return func(*args, **kwargs)
        wrapper.__signature__ = inspect.signature(func)  # type: ignore
        return typing.cast(typing.Callable[P, R], wrapper)
    return decorator


def itemgetter(mapping: typing.Mapping[str, typing.Any], *args: typing.Any) -> typing.Any:
    """Accumulative getitem.

    Parameters
    ----------
    obj : object
        The object to get the item

    Examples
    --------
    >>> obj = {
    ...     "foo": {
    ...         "bar": 3.14
    ...     }
    ... }
    >>> itemgetter(obj, "foo", "bar")
    ... 3.14

    Returns
    -------
    object
        The item value

    """
    for k in args:
        mapping = mapping[k]
    return mapping


def attrgetter(obj: typing.Any, *attrnames: str) -> typing.Any:
    """Get an accumulative attribute.

    Parameters
    ----------
    obj : object
        The object to get attribute

    Examples
    --------
    >>> @dataclass
    ... class Bar:
    ...     bar: str
    >>> @dataclass
    ... class Foo:
    ...     foo: Bar
    >>> obj = Foo(Bar("null value"))
    >>> attrgetter(obj, "foo", "bar")
    ... 'null value'

    Returns
    -------
    object
        The attribute value

    """
    for name in attrnames:
        obj = getattr(obj, name)
    return obj


class GenericProperty(typing.Generic[G, S]):
    def __init__(
        self,
        fget: typing.Callable[[typing.Any], G],
        fset: typing.Callable[[typing.Any, S], None]
    ) -> None:
        self.fget = fget
        self.fset = fset
        self.__doc__ = fget.__doc__

    @typing.overload
    def __get__(self, instance: None, owner: typing.Optional[type] = None) -> typing.Self: ...
    @typing.overload
    def __get__(self, instance: typing.Any, owner: typing.Optional[type] = None) -> G: ...
    def __get__(self, instance: typing.Optional[typing.Any], owner: typing.Optional[type] = None) -> typing.Union[G, typing.Self]:
        if instance is None:
            return self
        return self.fget(instance)

    def __set__(self, instance: typing.Any, value: S) -> None:
        self.fset(instance, value)

    def __delete__(self, instance: typing.Any) -> None:
        raise TypeError('Cannot delete a property')


def build_proxy_map(proxies: typing.Optional[ProxiesType]) -> typing.Dict[str, typing.Optional[httpx.URL]]:
    """Intern function to convert all proxy in a dict, to URL instance

    Parameters
    ----------
    proxies : `ProxiesType`, `None`
        The proxy dict.

    Returns
    -------
    dict[str, httpx.URL | None]
        The convertion result

    """
    if isinstance(proxies, typing.Mapping):
        return {str(key): httpx.URL(value) if isinstance(value, (str, httpx.URL)) else value for key, value in proxies.items()}
    else:
        return {"all://": httpx.URL(proxies) if isinstance(proxies, (str, httpx.URL)) else proxies}


def proxy_connect(url: typing.Union[httpx.URL, str], proxy: typing.Union[httpx.URL, str], proxy_timeout: typing.Optional[float] = None) -> socket.socket:
    """Create a proxy socket connection to a websocket url.

    Parameters
    ----------
    url : `httpx.URL`, `str`
        The websocket url.
    proxy : `httpx.URL`, `str`
        The proxy url. Supported protocols are: http, socks4, socks5
    proxy_timeout : `float`, `optional`
        The open-connection timeout. Default is `None`.

    Returns
    -------
    socket.socket
        The websocket connection.

    Raises
    ------
    ValueError
        if the proxy is not supported.

    """
    url, proxy = httpx.URL(url), httpx.URL(proxy)
    if not proxy.scheme.startswith(("http", "socks4", "socks5")):
        raise ValueError(f"Unsupported {proxy.scheme!r} protocol.") from None
    proxy_type = getattr(python_socks.ProxyType, proxy.scheme.upper().removesuffix("S"))
    ws_port = 443 if url.scheme.startswith("wss") else 80
    params: typing.Dict[str, typing.Any] = {
        "proxy_type": proxy_type,
        "host": proxy.host,
        "port": proxy.port or ws_port,
        "username": proxy.username or None,
        "password": proxy.password or None
    }
    proxy_socket = python_socks.sync.Proxy(proxy_type, proxy.host, proxy.port or ws_port, proxy.username or None, proxy.password or None)  # type: ignore
    return proxy_socket.connect(url.host, ws_port, proxy_timeout)  # type: ignore
