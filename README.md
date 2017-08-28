<a href="https://app.codesponsor.io/link/MY7qFCdB7bDgiBqdjtV9ASYi/suzaku/cachelper" rel="nofollow"><img src="https://app.codesponsor.io/embed/MY7qFCdB7bDgiBqdjtV9ASYi/suzaku/cachelper.svg" style="width: 888px; height: 68px;" alt="Sponsor" /></a>

cachelper
==========

[![Build Status](https://travis-ci.org/suzaku/cachelper.svg?branch=master)](https://travis-ci.org/suzaku/cachelper)

Useful cache helpers in one package!

## Install

```bash
pip install cachelper
```

## Helpers

### In memory cache

#### memoize

Caching function return values in memory.


```python

import cachelper

@cachelper.memoize()
def fibo(n):
    if n in (0, 1):
        return 1
    return fibo(n - 1) + fibo(n - 2)

fibo(10)
```

### Cache with Redis/Memcached

#### cache decorator

Add cache by decorating a function or method.

```python
from redis import StrictRedis
import cachelper

rds = StrictRedis()
cache = cachelper.RedisCache(rds)

@cache("key-{user_id}", timeout=300)
def get_name(user_id):
    # Fetch user name from database
    ...
```

The `RedisCache` used in the example above is a subclass of the [werkzeug one](http://werkzeug.pocoo.org/docs/0.12/contrib/cache/#werkzeug.contrib.cache.RedisCache).
It's just a mixin of the werkzeug implementation and `cachelper.HelperMixin`.


```python
class RedisCache(_RedisCache, HelperMixin):
    '''werkzeug.contrib.cache.RedisCache mixed with HelperMixin'''
```

You may use this mixin to create cache class of your own, as long as the following methods are provided:

- `get(key)`
- `set(key, value, timeout)`

#### cached function calls

Sometimes we don't want to cache all calls to a specific function.
So the decorator is not suitable, we may cache the call instead the function in this case:


```python
from redis import StrictRedis
import cachelper

rds = StrictRedis()
cache = cachelper.RedisCache(rds)

def get_name(user_id):
    # Fetch user name from database
    ...

user_id = 42
key = "key-{user_id}".format(user_id=user_id)
cache.call(lambda: get_name(user_id), key, timeout=300)
```

#### cached multiple calls

For most cache backends, it's much faster to get or set caches in bulk.

```python
from redis import StrictRedis
import cachelper

rds = StrictRedis()
cache = cachelper.RedisCache(rds)

def get_name(user_id):
    # Fetch user name from database
    ...

user_ids = [1, 2, 42, 1984]
names = cache.map("key-{user_id}", get_name, user_ids, timeout=300)
```
