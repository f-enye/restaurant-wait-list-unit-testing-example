from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Body:
    event_guid: str
    party_guid: str
    notification: str


def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper