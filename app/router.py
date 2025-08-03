import re
from typing import Callable, Optional

class Route:
    def __init__(self, method: str, pattern: str, handler: Callable):
        self.method = method.upper()
        self.pattern = pattern
        self.regex = re.compile(
            "^" + re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", pattern) + "$"
        )
        self.handler = handler

    def matches(self, method: str, path: str):
        if self.method != method.upper():
            return None
        match = self.regex.match(path)
        return match


class Router:
    def __init__(self):
        self.routes: list[Route] = []

    def add(self, method: str, pattern: str, handler: Callable):
        self.routes.append(Route(method, pattern, handler))

    def get(self, pattern: str):
        def wrapper(fn):
            self.add("GET", pattern, fn)
            return fn
        return wrapper

    def post(self, pattern: str):
        def wrapper(fn):
            self.add("POST", pattern, fn)
            return fn
        return wrapper

    def resolve(self, method: str, path: str) -> Optional[tuple[Callable, dict]]:
        for route in self.routes:
            match = route.matches(method, path)
            if match:
                return route.handler, match.groupdict()
        return None
