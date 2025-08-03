from typing import Callable, List
from app.request import Request
from app.response import Response

MiddlewareFunc = Callable[[Request, Response, Callable[[], Response]], Response]

class MiddlewareStack:
    def __init__(self):
        self._middlewares: List[MiddlewareFunc] = []

    def use(self, middleware: MiddlewareFunc):
        self._middlewares.append(middleware)

    def wrap(self, handler: Callable[[Request], Response]) -> Callable[[Request], Response]:
        def wrapped_handler(req: Request) -> Response:
            res = Response(b"")

            def build_chain(index: int):
                if index < len(self._middlewares):
                    def next_middleware():
                        return build_chain(index + 1)()
                    return lambda: self._middlewares[index](req, res, next_middleware)
                else:
                    return lambda: handler(req)

            return build_chain(0)()

        return wrapped_handler
