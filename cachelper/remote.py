import inspect
import functools

from werkzeug.contrib.cache import (
    RedisCache as _RedisCache,
    MemcachedCache as _MemcachedCache,
)


__all__ = ['HelperMixin', 'RedisCache']


class HelperMixin(object):

    '''A mixin class that add helpers to basic cache classes.

    Basic cache classes are classes with the following methods:

        - def get(self, key)
        - def set(self, key, value, timeout=None)
        - def delete(self, key)
    '''

    def call(self, func, key, timeout=None):
        '''Wraps a function call with cache.

        Args:
            func (function): the function to call.
            key (str): the cache key for this call.
            timeout (int): the cache timeout for the key (the
                           unit of this parameter depends on
                           the cache class you use, for example,
                           if you use the classes from werkzeug,
                           then timeout is in seconds.)

        Returns:
            The return value of calling func
        '''
        result = self.get(key)
        if result is None:
            result = func()
            self.set(key, result, timeout)
        return result

    def __call__(self, key_pattern, timeout=None):
        '''Use the cache object as a decorator factory.

        Args:
            key_pattern (str): the key pattern to use for generating
                               keys for caches of the decorated function
            timeout (int): the cache timeout for the key

        Returns:
            a decorator that cache return values of the decorated functions
            in keys generated based on the given key pattern
            and the calling args.

        Here's an example::

            @cache('key-name-for-{id}')
            def get_name(id):
                return 'name' + id
        '''

        def decorator(f):

            @functools.wraps(f)
            def _(*args, **kwargs):
                key = make_key(key_pattern, f, args, kwargs)

                def x():
                    return f(*args, **kwargs)

                return self.call(x, key, timeout)

            def clear(*args, **kwargs):
                key = make_key(key_pattern, f, args, kwargs)
                self.delete(key)

            _.clear_cachelper_cache = clear

            return _

        return decorator


class RedisCache(_RedisCache, HelperMixin):
    '''werkzeug.contrib.cache.RedisCache mixed with HelperMixin'''


class MemcachedCache(_MemcachedCache, HelperMixin):
    '''werkzeug.contrib.cache.MemcachedCache mixed with HelperMixin'''


def make_key(key_pattern, func, args, kwargs):
    callargs = inspect.getcallargs(func, *args, **kwargs)
    return key_pattern.format(**callargs)
