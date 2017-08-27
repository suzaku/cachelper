import time
import functools


__all__ = ['memoize']


def memoize(timeout=300):
    def decorator(f):
        cache = {}

        @functools.wraps(f)
        def _(*args, **kwargs):
            sorted_kw = sorted(kwargs.items())
            key = (args, tuple(sorted_kw))
            value, cache_time = cache.get(key, (None, None))
            now = time.time()
            if cache_time is None or (now - cache_time) > timeout:
                value, _ = cache[key] = (f(*args, **kwargs), now)
            return value

        _.clear_cachelper_cache = cache.clear

        return _

    return decorator
