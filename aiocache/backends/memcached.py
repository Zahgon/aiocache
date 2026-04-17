import asyncio
from typing import Optional

import aiomcache

from aiocache.base import BaseCache
from aiocache.serializers import JsonSerializer


class MemcachedCache(BaseCache[bytes]):
    """
    Memcached cache implementation with the following components as defaults:
        - serializer: :class:`aiocache.serializers.JsonSerializer`
        - plugins: []

    Config options are:

    :param serializer: obj derived from :class:`aiocache.serializers.BaseSerializer`.
    :param plugins: list of :class:`aiocache.plugins.BasePlugin` derived classes.
    :param namespace: string to use as default prefix for the key used in all operations of
        the backend. Default is an empty string, "".
    :param timeout: int or float in seconds specifying maximum timeout for the operations to last.
        By default its 5.
    :param endpoint: str with the endpoint to connect to. Default is 127.0.0.1.
    :param port: int with the port to connect to. Default is 11211.
    :param pool_size: int size for memcached connections pool. Default is 2.
    """

    NAME = "memcached"

    def __init__(self, host="127.0.0.1", port=11211, pool_size=2, **kwargs):
        if "serializer" not in kwargs:
            kwargs["serializer"] = JsonSerializer()

        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.pool_size = int(pool_size)
        self.client = aiomcache.Client(self.host, self.port, pool_size=self.pool_size)

    async def _get(self, key, encoding="utf-8", _conn=None):
        pass

    async def _gets(self, key, encoding="utf-8", _conn=None):
        pass

    async def _multi_get(self, keys, encoding="utf-8", _conn=None):
        pass

    async def _set(self, key, value, ttl=0, _cas_token=None, _conn=None):
        pass

    async def _cas(self, key, value, token, ttl=None, _conn=None):
        pass

    async def _multi_set(self, pairs, ttl=0, _conn=None):
        pass

    async def _add(self, key, value, ttl=0, _conn=None):
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

    async def _redlock_release(self, key, _):
        # Not ideal, should check the value coincides first but this would introduce
        # race conditions
        pass

    async def _close(self, *args, _conn=None, **kwargs):
        pass

    def build_key(self, key: str, namespace: Optional[str] = None) -> bytes:
        pass

    @classmethod
    def parse_uri_path(cls, path):
        pass

    def __repr__(self):  # pragma: no cover
        return "MemcachedCache ({}:{})".format(self.host, self.port)
