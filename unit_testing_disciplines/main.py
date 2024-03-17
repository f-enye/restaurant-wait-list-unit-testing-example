from fastapi import FastAPI
from pydantic import BaseModel

from unit_testing_disciplines.external.text.send import SendResult, send
from unit_testing_disciplines.external.waitlist.party.party_information import get_party
from unit_testing_disciplines.text.get_message import get_message

app = FastAPI()


class NotificationUpdate(BaseModel):
    event_guid: str
    party_guid: str
    notification: str


@app.post("/waitlist/party/notification/update")
def waitlist_party_notification_update(
    notification_update: NotificationUpdate,
) -> SendResult:
    return _waitlist_party_notification_update(notification_update)


def _waitlist_party_notification_update(notification_update: NotificationUpdate):
    party = get_party("", notification_update.party_guid)
    message = get_message(party, notification_update.notification)
    return send("", "sms", party.phone_number, "5555555552", message)
