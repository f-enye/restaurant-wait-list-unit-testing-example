from httpx import post
from pydantic import BaseModel


class SendResult(BaseModel):
    id: str  # The ID for the message
    status: str  # The status of the message (e.g. sent, queued, failed).


def send(
    api_key: str, protocol: str, to: str, from_: str, message: str
) -> SendResult:
    result = post(
        "https://t-e-x-t.example.com/send",
        headers={"X-API-KEY": api_key},
        data={
            "protocol": protocol,
            "to": to,
            "from": from_,
            "message": message,
        },
    )
    result.raise_for_status()
    response = result.json()
    return SendResult(
        id=response["id"],
        status=response["status"],
    )
