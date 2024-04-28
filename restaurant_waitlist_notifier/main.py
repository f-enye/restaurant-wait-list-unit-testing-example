from fastapi import FastAPI
from pydantic import BaseModel

from restaurant_waitlist_notifier.text_messages.get_message import get_message
from restaurant_waitlist_notifier.text_messages.send import SendResult, send
from restaurant_waitlist_notifier.waitlists.parties.get_party import get_party

app = FastAPI()


class StatusUpdatedEventRequest(BaseModel):
    event_id: str
    party_id: str
    status: str


@app.post("/waitlist/party/status/updated")
def waitlist_party_status_updated(
    event_request: StatusUpdatedEventRequest,
) -> SendResult:
    return _waitlist_party_status_updated(event_request)


def _waitlist_party_status_updated(event_request: StatusUpdatedEventRequest):
    party = get_party(event_request.party_id)
    message = get_message(party, event_request.status)
    return send("sms", party.phone_number, "5555555552", message)
