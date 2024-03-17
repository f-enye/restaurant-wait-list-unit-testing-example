from unit_testing_disciplines.external.example_framework.example_framework import Body
from unit_testing_disciplines.external.example_framework.example_framework import post
from unit_testing_disciplines.external.text.send import send, SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import get_party
from unit_testing_disciplines.text.get_message import get_message


@post(path="/waitlist/party/notification/update")
def waitlist_party_notification_update(body: Body) -> SendResult:
    return _waitlist_party_notification_update(body)

def _waitlist_party_notification_update(body: Body):
    party = get_party("", body.party_guid)
    message = get_message(party, body.notification)
    return send("", "sms", party.phone_number, "5555555552", message)
