import asyncio
import functools
import inspect
import logging

from aiocache.base import SENTINEL
from aiocache.lock import RedLock

logger = logging.getLogger(__name__)


class cached:
    """
    Caches the functions return value into a key generated with module_name, function_name
    and args. The cache is available in the function object as ``<function_name>.cache``.

    :param cache: cache instance to use when calling the ``set``/``get`` operations.
    :param ttl: int seconds to store the function call. Default is None which means no expiration.
    :param key_builder: Callable that allows to build the function dynamically. It receives
        the function plus same args and kwargs passed to the function.
        This behavior is necessarily different than ``BaseCache.build_key()``
    :param skip_cache_func: Callable that receives the result after calling the
        wrapped function and should return `True` if the value should skip the
        cache (or `False` to store in the cache).
        e.g. to avoid caching `None` results: `lambda r: r is None`
    :param noself: bool if you are decorating a class function, by default self is also used to
        generate the key. This will result in same function calls done by different class instances
        to use different cache keys. Use noself=True if you want to ignore it.
    """

    def __init__(
        self,
        cache,
        *,
        ttl=SENTINEL,
        key_builder=None,
        skip_cache_func=lambda x: False,
        noself=False,
    ):
        self.ttl = ttl
        self.key_builder = key_builder
        self.skip_cache_func = skip_cache_func
        self.noself = noself
        self.cache = cache

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            pass

        wrapper.cache = self.cache
        return wrapper

    async def decorator(
        self, f, *args, cache_read=True, cache_write=True, aiocache_wait_for_write=True, **kwargs
    ):
        pass

    def get_cache_key(self, f, args, kwargs):
        pass

    def _key_from_args(self, func, args, kwargs):
        pass

    async def get_from_cache(self, key):
        pass

    async def set_in_cache(self, key, value):
        pass


class cached_stampede(cached):
    """
    Caches the functions return value into a key generated with module_name, function_name and args
    while avoids for cache stampede effects.

    :param cache: cache instance to use when calling the ``set``/``get`` operations.
        Default is :class:`aiocache.SimpleMemoryCache`.
    :param lease: int seconds to lock function call to avoid cache stampede effects.
        If 0 or None, no locking happens (default is 2). valkey and memory backends support
        float ttls
    :param ttl: int seconds to store the function call. Default is None which means no expiration.
    :param key_from_attr: str arg or kwarg name from the function to use as a key.
    :param key_builder: Callable that allows to build the function dynamically. It receives
        the function plus same args and kwargs passed to the function.
        This behavior is necessarily different than ``BaseCache.build_key()``
    :param skip_cache_func: Callable that receives the result after calling the
        wrapped function and should return `True` if the value should skip the
        cache (or `False` to store in the cache).
        e.g. to avoid caching `None` results: `lambda r: r is None`
    :param noself: bool if you are decorating a class function, by default self is also used to
        generate the key. This will result in same function calls done by different class instances
        to use different cache keys. Use noself=True if you want to ignore it.
    """

    def __init__(self, cache, lease=2, **kwargs):
        super().__init__(cache, **kwargs)
        self.lease = lease

    async def decorator(self, f, *args, **kwargs):
        pass


def _get_args_dict(func, args, kwargs):
    pass


class multi_cached:
    """
    Only supports functions that return dict-like structures. This decorator caches each key/value
    of the dict-like object returned by the function. The dict keys of the returned data should
    match the set of keys that are passed to the decorated callable in an iterable object.
    The name of that argument is passed to this decorator via the parameter
    ``keys_from_attr``. ``keys_from_attr`` can be the name of a positional or keyword argument.

    If the argument specified by ``keys_from_attr`` is an empty list, the cache will be ignored
    and the function will be called. If only some of the keys in ``keys_from_attr``are cached
    (and ``cache_read`` is True) those values will be fetched from the cache, and only the
    uncached keys will be passed to the callable via the argument specified by ``keys_from_attr``.

    By default, the callable's name and call signature are not incorporated into the cache key,
    so if there is another cached function returning a dict with same keys, those keys will be
    overwritten. To avoid this, use a specific ``namespace`` in each cache decorator or pass a
    ``key_builder``.

    If ``key_builder`` is passed, then the values of ``keys_from_attr`` will be transformed
    before requesting them from the cache. Equivalently, the keys in the dict-like mapping
    returned by the decorated callable will be transformed before storing them in the cache.

    The cache is available in the function object as ``<function_name>.cache``.

    Extra args that are injected in the function that you can use to control the cache
    behavior are:

        - ``cache_read``: Controls whether the function call will try to read from cache first or
                          not. Enabled by default.
        - ``cache_write``: Controls whether the function call will try to write in the cache once
                           the result has been retrieved. Enabled by default.
        - ``aiocache_wait_for_write``: Controls whether the call of the function will wait for the
                                       value in the cache to be written. If set to False, the write
                                       happens in the background. Enabled by default

    :param cache: cache instance to use when calling the ``multi_set``/``multi_get`` operations.
    :param keys_from_attr: name of the arg or kwarg in the decorated callable that contains
        an iterable that yields the keys returned by the decorated callable.
    :param key_builder: Callable that enables mapping the decorated function's keys to the keys
        used by the cache. Receives a key from the iterable corresponding to
        ``keys_from_attr``, the decorated callable, and the positional and keyword arguments
        that were passed to the decorated callable. This behavior is necessarily different than
        ``BaseCache.build_key()`` and the call signature differs from ``cached.key_builder``.
    :param skip_cache_func: Callable that receives both key and value and returns True
        if that key-value pair should not be cached (or False to store in cache).
        The keys and values to be passed are taken from the wrapped function result.
    :param ttl: int seconds to store the keys. Default is 0 which means no expiration.
    """

    def __init__(
        self,
        cache=None,
        *,
        keys_from_attr,
        key_builder=None,
        skip_cache_func=lambda k, v: False,
        ttl=SENTINEL,
    ):
        self.cache = cache
        self.keys_from_attr = keys_from_attr
        self.key_builder = key_builder or (lambda key, f, *args, **kwargs: key)
        self.skip_cache_func = skip_cache_func
        self.ttl = ttl

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            pass

        wrapper.cache = self.cache
        return wrapper

    async def decorator(
        self, f, *args, cache_read=True, cache_write=True, aiocache_wait_for_write=True, **kwargs
    ):
        pass

    def get_cache_keys(self, f, args, kwargs):
        pass

    async def get_from_cache(self, *keys):
        pass

    async def set_in_cache(self, result, fn, fn_args, fn_kwargs):
        pass
