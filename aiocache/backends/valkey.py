import logging
import sys
from typing import Optional

from glide import (
    Batch,
    ConditionalChange,
    ExpirySet,
    ExpiryType,
    GlideClient,
    GlideClientConfiguration,
)
from glide.exceptions import RequestError as IncrbyException

from aiocache.base import BaseCache
from aiocache.serializers import JsonSerializer

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing import Any as Self


logger = logging.getLogger(__name__)


class ValkeyCache(BaseCache[str]):
    """
    Valkey cache implementation with the following components as defaults:
        - serializer: :class:`aiocache.serializers.JsonSerializer`
        - plugins: []

    Config options are:

    :param serializer: obj derived from :class:`aiocache.serializers.BaseSerializer`.
    :param plugins: list of :class:`aiocache.plugins.BasePlugin` derived classes.
    :param namespace: string to use as default prefix for the key used in all operations of
        the backend. Default is an empty string, "".
    :param timeout: int or float in seconds specifying maximum timeout for the operations to last.
        By default its 5.
    :param client: glide.GlideClient which is an active client for working with valkey
    """

    NAME = "valkey"

    def __init__(
        self, config: GlideClientConfiguration, **kwargs
    ):
        self.config = config

        if "serializer" not in kwargs:
            kwargs["serializer"] = JsonSerializer()
        if "key_builder" not in kwargs:
            kwargs["key_builder"] = lambda k, ns: f"{ns}:{k}" if ns else k

        super().__init__(**kwargs)

    async def __aenter__(self) -> Self:
        self.client = await GlideClient.create(self.config)
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.client.close()

    async def _get(self, key, encoding="utf-8", _conn=None):
        pass

    _gets = _get

    async def _multi_get(self, keys, encoding="utf-8", _conn=None):
        pass

    async def _set(self, key, value, ttl=None, _cas_token=None, _conn=None):
        pass

    async def _cas(self, key, value, token, ttl=None, _conn=None):
        pass

    async def _multi_set(self, pairs, ttl=None, _conn=None):
        pass

    async def __multi_set_ttl(self, values, ttl):
        pass

    async def _add(self, key, value, ttl=None, _conn=None):
        pass

    async def _exists(self, key, _conn=None):
        pass

    async def _increment(self, key, delta, _conn=None):
        pass

    async def _expire(self, key, ttl, _conn=None):
        pass

    async def _delete(self, key, _conn=None):
        pass

    async def _clear(self, namespace=None, _conn=None):
        pass

    async def _raw(self, command, *args, encoding="utf-8", _conn=None, **kwargs):
        pass

    async def _redlock_release(self, key, value):
        pass

    def build_key(self, key: str, namespace: Optional[str] = None) -> str:
        pass

    @classmethod
    def parse_uri_path(cls, path):
        """
        Given a uri path, return the Valkey specific configuration
        options in that path string according to iana definition
        http://www.iana.org/assignments/uri-schemes/prov/redis

        :param path: string containing the path. Example: "/0"
        :return: mapping containing the options. Example: {"db": "0"}
        """
        pass

    def __repr__(self):  # pragma: no cover
        return (
            f"ValkeyCache ({self.client.config.addresses[0].host}"
            f":{self.client.config.addresses[0].port})"
        )
