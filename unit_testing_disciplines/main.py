from dataclasses import dataclass
from typing import Any, Callable
from unit_testing_disciplines.external.text.send import send, SendResult

def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    to: str
    from_: str
    text: str


@post(path="/send-text")
def send_text(body: Body) -> SendResult:
    return send("", "sms", body.to, body.from_, body.text)
    


