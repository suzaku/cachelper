cachelper
##########

.. image:: https://travis-ci.org/suzaku/cachelper.svg?branch=master
    :target: https://travis-ci.org/suzaku/cachelper
.. image:: https://img.shields.io/pypi/v/cachelper.svg
    :target: https://pypi.python.org/pypi/cachelper

Useful cache helpers in one package!

.. image:: https://app.codesponsor.io/embed/MY7qFCdB7bDgiBqdjtV9ASYi/suzaku/cachelper.svg
    :width: 888px
    :height: 68px
    :alt: Sponsor
    :target: https://app.codesponsor.io/link/MY7qFCdB7bDgiBqdjtV9ASYi/suzaku/cachelper

Install
*******

.. code-block:: bash

    pip install cachelper

Helpers
*******

In memory cache
===============

memoize
---------------

Caching function return values in memory.


.. code-block:: python

    import cachelper

    @cachelper.memoize()
    def fibo(n):
        if n in (0, 1):
            return 1
        return fibo(n - 1) + fibo(n - 2)

    fibo(10)

Cache with Redis/Memcached
==============================

cache decorator
---------------

Add cache by decorating a function or method.

.. code-block:: python

    from redis import StrictRedis
    from werkzeug.contrib.cache import RedisCache as _RedisCache

    import cachelper

    class RedisCache(_RedisCache, HelperMixin):
        '''werkzeug.contrib.cache.RedisCache mixed with HelperMixin'''

        def get_many(self, keys):
            return super().get_many(*keys)

    rds = StrictRedis()
    cache = RedisCache(rds)

    @cache("key-{user_id}", timeout=300)
    def get_name(user_id):
        # Fetch user name from database
        ...


You may use this mixin to create cache class of your own, as long as the following methods are provided:

- ``def get(self, key)``
- ``def set(self, key, value, timeout=None)``
- ``def delete(self, key)``
- ``def get_many(self, keys)``
- ``def set_many(self, mapping, timeout=None)``

cached function calls
------------------------------

Sometimes we don't want to cache all calls to a specific function.
So the decorator is not suitable, we may cache the call instead the function in this case:


.. code-block:: python

    def get_name(user_id):
        # Fetch user name from database
        ...

    user_id = 42
    key = "key-{user_id}".format(user_id=user_id)
    cache.call(lambda: get_name(user_id), key, timeout=300)

cached multiple calls
------------------------------

For most cache backends, it's much faster to get or set caches in bulk.

.. code-block:: python

    def get_name(user_id):
        # Fetch user name from database
        ...

    user_ids = [1, 2, 42, 1984]
    names = cache.map("key-{user_id}", get_name, user_ids, timeout=300)
