from dataclasses import dataclass
from typing import Any, Callable


def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    text: str


@post(path="/send-text")
def send_text(body: Body) -> dict[str, Body]:
    return {"body": body}
