import re
import typing as t

from visapi.exceptions import MethodNotAllowed, NotFound
from visapi.routing.convertor import Convertor

build_rule_regex = re.compile(
    r"(?P<static>[^{]*){(?P<var>[a-zA-Z_][a-zA-Z_0-9]*):(?P<convertor>[a-zA-Z_][a-zA-Z_0-9]*)}"
)


def get_rule_part(rule_path: str):
    start = 0
    end = len(rule_path)
    while start < end:
        res = build_rule_regex.search(rule_path, pos=start)
        if not res:
            break
        group_dict = res.groupdict()
        yield group_dict["static"], group_dict["var"], group_dict["convertor"]
        start = res.end()
    if start < end:
        legacy_route = rule_path[start:]
        if '{' in legacy_route or '}' in legacy_route:
            raise SyntaxError(f'Incorrect rule syntax. Should not appear single "{" or "}" in {legacy_route}')
        yield legacy_route, None, None


class Route:
    protocol: str = None
    partial_route: bool = False

    def __init__(self, rule_path: str, callback: callable, name: str):
        self.rule_path: str = rule_path
        self.callback: t.Callable = callback
        self.name: str = name
        self.dynamic: t.Dict = {}
        self.regex: t.Optional[re.Pattern] = None
        self.build()

    def build(self):
        regex_part = []
        for static, variable, convertor_name in get_rule_part(self.rule_path):
            # we need escape plain string
            regex_part.append(re.escape(static))
            if convertor_name is None:
                continue
            if variable in self.dynamic:
                raise SyntaxError(f"Duplicate keyword parameters '{variable}' cannot appear in same route path")
            convertor = convertors.get(convertor_name, None)
            if convertor is None:
                raise SyntaxError(f" convertor '{convertor_name}' does not exist.")
            self.dynamic[variable] = convertor
            regex_part.append(f"(?P<{variable}>{convertor.regex})")
        regex_str = f"^{''.join(regex_part)}"
        if not self.partial_route:
            regex_str += "$"
        self.regex = re.compile(regex_str)

    def handle(self, *args, **kwargs):
        raise NotImplementedError("Subclass must implement this method")


class GroupRoute(Route):
    partial_route = True

    async def handle(self, scope, receive, send, **kwargs):
        if not (res := self.regex.match(scope["path"])):
            raise NotFound()
        scope["group_route"] = dict(path_match_end=res.end())
        return await self.callback(scope, receive, send, **res.groupdict())


class HTTPRoute(Route):
    protocol = "HTTP"

    def __init__(self, rule_path: str, methods: t.List[str], callback: t.Callable, name: str):
        methods = [str(method).upper() for method in methods]
        assert methods, "Methods must be HTTP protocol method list"
        self.methods = methods
        super().__init__(rule_path, callback, name)

    async def handle(self, scope, receive, send, **kwargs):
        path = scope["path"]
        if group_route := scope.get("group_route", {}):
            path = path[group_route.get("path_match_end"):]
        if not (res := self.regex.match(path)):
            raise NotFound()
        kwargs |= res.groupdict()
        if method := scope["method"] not in self.methods:
            raise MethodNotAllowed(method, self.methods)
        await self.callback(scope, receive, send, **kwargs)


class WebSocketRoute(Route):
    protocol = "WebSocket"

    async def handle(self, scope, receive, send, **kwargs):
        path = scope["path"]
        if group_route := scope.get("group_route", {}):
            path = path[group_route.get("path_match_end"):]
        if not (res := self.regex.match(path)):
            raise NotFound()
        kwargs |= res.groupdict()
        await self.callback(scope, receive, send, **kwargs)
