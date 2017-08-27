import inspect
import functools

from werkzeug.contrib.cache import RedisCache as _RedisCache


__all__ = ['HelperMixin', 'RedisCache']


class HelperMixin(object):

    def call(self, func, key, timeout=None):
        result = self.get(key)
        if result is None:
            result = func()
            self.set(key, result, timeout)
        return result

    def __call__(self, key_pattern, timeout=None):

        def decorator(f):

            @functools.wraps(f)
            def _(*args, **kwargs):
                key = make_key(key_pattern, f, args, kwargs)

                def x():
                    return f(*args, **kwargs)

                return self.call(x, key, timeout)

            return _

        return decorator


class RedisCache(_RedisCache, HelperMixin):
    pass


def make_key(key_pattern, func, args, kwargs):
    callargs = inspect.getcallargs(func, *args, **kwargs)
    return key_pattern.format(**callargs)
