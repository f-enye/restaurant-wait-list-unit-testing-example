from dataclasses import dataclass
from typing import Any, Callable
from unit_testing_disciplines.external.text.send import send, SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import getPartyInformation

def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    eventGuid: str
    partyGuid: str
    notification: str # consider the following notifications, added-to-waitlist, table-prepared, delayed

def getMessage(status: str):
    return "Hello"

@post(path="/waitlist/party/notification/update")
def send_text(body: Body) -> SendResult:
    party = getPartyInformation(body.partyGuid)
    message = getMessage(body.notification)
    return send("", "sms", party.phone_number, "5555555552", message)
    


