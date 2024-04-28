from fastapi import FastAPI
from pydantic import BaseModel

from restaurant_waitlist_notifier.text_messages.get_message import get_message
from restaurant_waitlist_notifier.text_messages.send import SendResult, send
from restaurant_waitlist_notifier.waitlists.parties.get_party import get_party

app = FastAPI()


class Notification(BaseModel):
    event_id: str
    party_id: str
    type: str


@app.post("/waitlist/party/notification/sent")
def waitlist_party_notification_sent(
    notification: Notification,
) -> SendResult:
    return _waitlist_party_notification_sent(notification)


def _waitlist_party_notification_sent(notification: Notification):
    party = get_party(notification.party_id)
    message = get_message(party, notification.type)
    return send("sms", party.phone_number, "5555555552", message)
