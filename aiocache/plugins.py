"""
This module implements different plugins you can attach to your cache instance. They
are coded in a collaborative so you can use multiple inheritance.
"""

from aiocache.base import API


class BasePlugin:
    @classmethod
    def add_hook(cls, func, hooks):
        for hook in hooks:
            setattr(cls, hook, func)

    async def do_nothing(self, *args, **kwargs):
        pass


BasePlugin.add_hook(
    BasePlugin.do_nothing, ["pre_{}".format(method.__name__) for method in API.CMDS]
)
BasePlugin.add_hook(
    BasePlugin.do_nothing, ["post_{}".format(method.__name__) for method in API.CMDS]
)


class TimingPlugin(BasePlugin):
    """
    Calculates average, min and max times each command takes. The data is saved
    in the cache class as a dict attribute called ``profiling``. For example, to
    access the average time of the operation get, you can do ``cache.profiling['get_avg']``
    """

    @classmethod
    def save_time(cls, method):
        pass


for method in API.CMDS:
    TimingPlugin.add_hook(
        TimingPlugin.save_time(method.__name__), ["post_{}".format(method.__name__)]
    )


class HitMissRatioPlugin(BasePlugin):
    """
    Calculates the ratio of hits the cache has. The data is saved in the cache class as a dict
    attribute called ``hit_miss_ratio``. For example, to access the hit ratio of the cache,
    you can do ``cache.hit_miss_ratio['hit_ratio']``. It also provides the "total" and "hits"
    keys.
    """

    async def post_get(self, client, key, took=0, ret=None, **kwargs):
        pass

    async def post_multi_get(self, client, keys, took=0, ret=None, **kwargs):
        pass
