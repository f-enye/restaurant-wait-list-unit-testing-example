from dataclasses import dataclass
from typing import Any, Callable
from unit_testing_disciplines.external.text.send import send, SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import get_party
from unit_testing_disciplines.text.get_message import get_message


def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    event_guid: str
    party_guid: str
    notification: str


@post(path="/waitlist/party/notification/update")
def waitlist_party_notification_update(body: Body) -> SendResult:
    party = get_party("", body.party_guid)
    message = get_message(party, body.notification)
    return send("", "sms", party.phone_number, "5555555552", message)
