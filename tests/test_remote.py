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


def test_decorator(redis, mocker):
    tracker = mocker.Mock()
    cache = cachelper.RedisCache(redis)

    @cache("key-{first}-{last}", timeout=300)
    def get_name(first, last):
        tracker()
        return first + ' ' + last

    assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
    assert get_name('Kujo', 'Jotaro') == 'Kujo Jotaro'
    assert tracker.call_count == 1
