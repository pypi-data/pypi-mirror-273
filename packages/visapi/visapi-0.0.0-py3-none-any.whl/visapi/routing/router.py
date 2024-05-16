import inspect
import typing as t
from functools import update_wrapper

from visapi.exceptions import NotFound, MethodNotAllowed
from visapi.routing.route import HTTPRoute, WebSocketRoute, GroupRoute, Route
from visapi.utils.arguments import accept_arguments, accept_var_key_word_argument


class Router:
    route_cls = HTTPRoute
    ws_route_cls = WebSocketRoute
    group_route_cls = GroupRoute

    def __init__(self):
        self.name_set = set()
        self.path_namespace = set()
        self.routes = []

    def _validate_route_param(self, rule_path: str, name: str, callback: callable, protocol: t.Optional[str] = ""):
        # The route path must start with /
        assert rule_path.startswith(
            '/'), f'The route "{rule_path}" of the {callback!r} callback should start with "/"'
        # enable to solve different protocol can not appear same route path
        rule_path_namespace = f"{protocol}:{rule_path}"
        if rule_path_namespace in self.path_namespace:
            raise ValueError('"%s" This route path is already in the router.' % rule_path)
        self.path_namespace.add(rule_path_namespace)
        if name in self.name_set:
            ValueError('"%s" This name is already in the router.' % name)
        self.name_set.add(name)

    def _validate_parameter(self, callback, parameters):
        if (
                not accept_arguments(callback, parameters)
                and
                not accept_var_key_word_argument(callback)
        ):
            raise ValueError(
                f"You should provide positional parameters such as {','.join(parameters)}."
                f" or provide a keyword variable parameter to the callback '{callback.__name__}'")

    def route(self, rule_path: str, methods: t.List[str], name: t.Optional[str] = None):
        def inner(callback: t.Callable):
            update_wrapper(inner, callback)
            name_ = name or callback.__name__
            self._validate_route_param(rule_path, name_, callback, self.route_cls.protocol)
            route = self.route_cls(rule_path, methods, callback, name)
            self._validate_parameter(callback, route.dynamic.keys())
            self.routes.append(route)
            return callback

        return inner

    def websocket(self, rule_path: str, name: t.Optional[str] = None):
        def inner(callback: t.Callable):
            if not inspect.iscoroutinefunction(callback):
                raise ValueError("WebSocket callback should be a coroutine function.")
            update_wrapper(inner, callback)
            name_ = name or callback.__name__
            self._validate_route_param(rule_path, name_, callback, self.ws_route_cls.protocol)
            route = self.ws_route_cls(rule_path, callback, name)
            self._validate_parameter(callback, route.dynamic.keys())
            self.routes.append(route)
            return callback

        return inner

    def get(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["GET"], name=name)

    def post(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["POST"], name=name)

    def put(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["PUT"], name=name)

    def delete(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["DELETE"], name=name)

    def patch(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["PATCH"], name=name)

    def options(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["OPTIONS"], name=name)

    def head(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["HEAD"], name=name)

    def trace(self, rule_path: str, name: t.Optional[str] = None):
        return self.route(rule_path, methods=["TRACE"], name=name)

    def group(self, group: "GroupRouter"):
        self._validate_route_param(group.prefix, group.name, group, self.group_route_cls.protocol)
        route = self.group_route_cls(group.prefix, group, group.name)
        self.routes.append(route)

    def middleware(self, middleware):
        def inner(func):
            pass

        return inner

    async def __call__(self, scope, receive, send, **kwargs):
        # TODO do not use catch error！！！
        for route in self.routes:
            try:
                res = await route.handle(scope, receive, send, **kwargs)
            except NotFound as e:
                continue
            except MethodNotAllowed as e:
                raise
            except Exception as e:
                raise
            else:
                return res
        raise NotFound


class GroupRouter(Router):
    def __init__(self, name: str, prefix: str = None):
        self.name = name
        self.prefix = prefix or ""
        super().__init__()
