from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from unit_testing_disciplines.external.text.send import send, SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import (
    Party,
    get_party,
)


def post(path: str) -> Callable[..., Any]:
    def _wrapper(f: Callable[..., Any]) -> Callable[..., Any]:
        return f

    return _wrapper


@dataclass(frozen=True)
class Body:
    event_guid: str
    party_guid: str
    notification: str  # consider the following notifications, added_to_waitlist, table_prepared, waitlist_delayed

def get_added_to_waitlist_message(party: Party) -> str:
    return f"Welcome, we've added you to our waitlist. We expect to have your table prepared in about {party.quoted_time_in_minutes} minutes."

def get_table_prepared_message(party: Party) -> str:
    return "Hello, you're table is ready. To get seated please see the host."

class Notifications(Enum):
    added_to_waitlist = "added_to_waitlist"
    table_prepared = "table_prepared"
    waitlist_delayed = "waitlist_delayed"
    
_strategies = {
    Notifications.added_to_waitlist: get_added_to_waitlist_message,
    Notifications.table_prepared: get_table_prepared_message
}

def get_message(party: Party, notification: str) -> str:
    return _strategies[Notifications(notification)](party)


@post(path="/waitlist/party/notification/update")
def waitlist_party_notification_update(body: Body) -> SendResult:
    party = get_party("", body.party_guid)
    message = get_message(party, body.notification)
    return send("", "sms", party.phone_number, "5555555552", message)
