import time

import pytest
from redislite import StrictRedis

import cachelper


@pytest.fixture()
def redis(tmpdir):
    yield StrictRedis(str(tmpdir.join('redis.db')))


class TestCacheCall:

    def test_should_cache_result(self, redis, mocker):
        key = 'some-key'
        func = mocker.Mock()
        ret = func.return_value = {'name': 'Jojo'}

        cache = cachelper.RedisCache(redis)
        assert cache.call(func, key) == ret
        assert cache.call(func, key) == ret
        assert func.call_count == 1


def test_cache_map(redis, mocker):
    tracker = mocker.Mock()
    cache = cachelper.RedisCache(redis)

    def add(a, b):
        tracker()
        if a == 5:
            return None
        return a + b

    key_pat = "key-{a}-{b}"

    assert cache.map(key_pat, add, [(1, 2), (3, 4), (5, 1)]) == [3, 7, None]
    assert cache.map(key_pat, add, [(1, 2), (3, 4), (5, 1)]) == [3, 7, None]
    assert tracker.call_count == 3

    assert cache.map(key_pat, add, [(10, 10), (1, 2)]) == [20, 3]
    assert tracker.call_count == 4


class TestDecorator:

    def test_should_cache_result(self, redis, mocker):
        tracker = mocker.Mock()
        cache = cachelper.RedisCache(redis)

        @cache("key-{first}-{last}", timeout=300)
        def get_name(first, last):
            tracker()
            return first + ' ' + last

        assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
        assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
        assert tracker.call_count == 1

    def test_should_cache_empty_result(self, redis, mocker):
        tracker = mocker.Mock()
        cache = cachelper.RedisCache(redis)

        @cache("key-{first}-{last}", timeout=300)
        def get_name(first, last):
            tracker()
            return None

        assert get_name('Kujo', 'Jotaro') is None
        assert get_name('Kujo', 'Jotaro') is None
        assert tracker.call_count == 1

    def test_can_clear_cache(self, redis, mocker):
        tracker = mocker.Mock()
        cache = cachelper.RedisCache(redis)

        @cache("key-{first}-{last}", timeout=300)
        def get_name(first, last):
            tracker()
            return first + ' ' + last

        assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
        get_name.clear_cachelper_cache('Kujo', 'Jotaro')
        assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
        assert tracker.call_count == 2
