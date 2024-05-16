import typing as t

from visapi.context import application
from visapi.routing.router import Router


class VisAPI:

    def __init__(self, router_cls: Router = None, config=None):
        super().__init__()
        self.router_cls = router_cls
        token = application.set(self)

    def route(self, *args, **kwargs):
        return self.router_cls.route(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        pass
