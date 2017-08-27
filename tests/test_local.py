import cachelper


class TestMemorize:

    def test_should_cache_return_value(self, mocker):
        func = mocker.Mock()
        func.side_effect = lambda i: i * 2
        func.__name__ = 'double'

        cached = cachelper.memoize()(func)
        assert cached(2) == 4
        assert cached(2) == 4
        assert func.call_count == 1
        assert cached(4) == 8
        assert cached(4) == 8
        assert func.call_count == 2

    def test_can_clear_cache(self, mocker):
        func = mocker.Mock()
        func.side_effect = lambda i: i * 2
        func.__name__ = 'double'

        decorator = cachelper.memoize()
        cached = decorator(func)
        cached(10)
        cached.clear_cachelper_cache()
        cached(10)
        assert func.call_count == 2
