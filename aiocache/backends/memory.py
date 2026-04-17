import asyncio
from typing import Optional, OrderedDict

from aiocache.base import BaseCache
from aiocache.serializers import NullSerializer


class SimpleMemoryCache(BaseCache[str]):
    """
    Memory cache implementation with the following components as defaults:
        - serializer: :class:`aiocache.serializers.NullSerializer`
        - plugins: None
        - backend: dict

    Config options are:

    :param serializer: obj derived from :class:`aiocache.serializers.BaseSerializer`.
    :param plugins: list of :class:`aiocache.plugins.BasePlugin` derived classes.
    :param namespace: string to use as default prefix for the key used in all operations of
        the backend. Default is an empty string, "".
    :param timeout: int or float in seconds specifying maximum timeout for the operations to last.
        By default, its 5.
    :param maxsize: int maximum number of keys to store (None for unlimited)
    """

    NAME = "memory"

    # TODO(PY312): https://peps.python.org/pep-0692/
    def __init__(self, **kwargs):
        # Extract maxsize before passing kwargs to base class
        self.maxsize = kwargs.pop('maxsize', None)
        if "serializer" not in kwargs:
            kwargs["serializer"] = NullSerializer()
        super().__init__(**kwargs)

        self._cache: OrderedDict[str, object] = OrderedDict()
        self._handlers: dict[str, asyncio.TimerHandle] = {}

    def _mark_accessed(self, key: str) -> None:
        """Move key to end to mark as recently used."""
        pass

    def _evict_if_needed(self) -> None:
        """Evict least recently used items if over maxsize."""
        pass

    async def _get(self, key, encoding="utf-8", _conn=None):
        pass

    async def _gets(self, key, encoding="utf-8", _conn=None):
        pass

    async def _multi_get(self, keys, encoding="utf-8", _conn=None):
        pass

    async def _set(self, key, value, ttl=None, _cas_token=None, _conn=None):
        pass

    async def _multi_set(self, pairs, ttl=None, _conn=None):
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

    def __delete(self, key):
        pass

    def build_key(self, key: str, namespace: Optional[str] = None) -> str:
        pass

    @classmethod
    def parse_uri_path(cls, path):
        pass
