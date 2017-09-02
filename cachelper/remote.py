import inspect
import functools


__all__ = ['HelperMixin']


class HelperMixin(object):

    '''A mixin class that add helpers to basic cache classes.

    Basic cache classes are classes with the following methods:

        - def get(self, key)
        - def set(self, key, value, timeout=None)
        - def delete(self, key)
        - def get_dict(self, keys)
        - def set_many(self, mapping, timeout=None)
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
        if result == NONE_RESULT:
            return None
        if result is None:
            result = func()
            self.set(
                key,
                result if result is not None else NONE_RESULT,
                timeout
            )
        return result

    def map(self, key_pattern, func, all_args, timeout=None):
        '''Cache return value of multiple calls.

        Args:
            key_pattern (str): the key pattern to use for generating
                               keys for caches of the decorated function.
            func (function): the function to call.
            all_args (list): a list of args to be used to make calls to
                             the function.
            timeout (int): the cache timeout

        Returns:
            A list of the return values of the calls.

        Example::

            def add(a, b):
                return a + b

            cache.map(key_pat, add, [(1, 2), (3, 4)]) == [3, 7]
        '''
        results = []
        keys = [
            make_key(key_pattern, func, args, {})
            for args in all_args
        ]
        cached = dict(zip(keys, self.get_many(keys)))
        cache_to_add = {}
        for key, args in zip(keys, all_args):
            val = cached[key]
            if val is None:
                val = func(*args)
                cache_to_add[key] = val if val is not None else NONE_RESULT
            if val == NONE_RESULT:
                val = None
            results.append(val)
        if cache_to_add:
            self.set_many(cache_to_add, timeout)
        return results

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


def make_key(key_pattern, func, args, kwargs):
    callargs = inspect.getcallargs(func, *args, **kwargs)
    return key_pattern.format(**callargs)


class Empty(object):

    obj = None

    def __new__(cls):
        if not cls.obj:
            cls.obj = object.__new__(cls)
        return cls.obj

    def __eq__(self, other):
        return isinstance(other, Empty)

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return False

    def __str__(self):
        return "<Empty: I'm nothing.>"

    __repr__ = __str__


NONE_RESULT = Empty()
