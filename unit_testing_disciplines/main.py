from dataclasses import dataclass
from typing import Any, Callable
import requests
from dataclasses import dataclass

def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    to: str
    from_: str
    text: str


@dataclass(frozen=True)
class SendResult:
    id: str  # The ID for the message
    status: str  # The status of the message (e.g. sent, queued, failed).


@post(path="/send-text")
def send_text(body: Body) -> SendResult:
    return send("", "sms", body.to, body.from_, body.text)
    

def send(
    bearer_token: str, 
    protocol: str, 
    to: str,
    from_: str,
    message: str
) -> SendResult:  
    result = requests.post(
        "https://t-e-x-t.example.com/send", 
        headers={"Authorization": f"Bearer {bearer_token}"}, 
        data={
            "protocol": protocol,
            "to": to,
            "from": from_,
            "message": message,
        }
    )
    result.raise_for_status()
    response = result.json()
    return SendResult(
        id=response["id"], 
        status=response["status"],
    )

