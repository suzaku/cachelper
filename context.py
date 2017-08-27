import threading
from contextlib import contextmanager


class Local(threading.local):

    def __init__(self):
        self.top_ctx = None

data = Local()
top_ctx = None


class ContextManager(object):

    def __getattr__(self, name):
        ctx = data.top_ctx
        while ctx:
            if hasattr(ctx, name):
                return getattr(ctx, name)
            ctx = ctx.parent
        raise AttributeError(name)

    def __setattr__(self, name, value):
        setattr(data.top_ctx, name, value)


class Context(dict):

    def __init__(self, parent):
        self.parent = parent
        super(dict, self).__init__()

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


@contextmanager
def new_context(**kwargs):
    orig_top = top_ctx
    ctx = Context(data.top_ctx)
    ctx.update(kwargs)
    data.top_ctx = ctx
    try:
        yield ctx
    finally:
        data.top_ctx = orig_top

cur_context = ContextManager()
