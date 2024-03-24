from datetime import datetime
import json
from unittest.mock import ANY, patch

import respx
from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture

from unit_testing_disciplines.external.text.send import SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import Party
from unit_testing_disciplines.main import NotificationUpdate, app


@fixture
def send_mock():
    with patch(
        "unit_testing_disciplines.main.send",
        return_value=SendResult(id="1", status="sent"),
    ) as mock:
        yield mock


@fixture
def get_waitlist_secrets_mock():
    with patch(
        "unit_testing_disciplines.external.waitlist.party.party_information.get_secrets",
        return_value="example-waitlist-api-key",
    ) as mock:
        yield mock


@fixture
def get_party_mock(get_waitlist_secrets_mock):
    response = Response(
        200,
        json={
            "name": "Peter",
            "phone_number": "5555555551",
            "time_of_arrival": str(datetime(2024, 1, 1, 1, 0)),
            "size": 1,
            "quoted_time_in_minutes": 30,
        },
    )

    with respx.mock(base_url="https://waitlist.example.com/party/") as mock:
        mock.get(name="get-waitlist-party", path__regex=r".+") % response
        yield mock


@fixture
def get_text_secrets_mock():
    with patch(
        "unit_testing_disciplines.external.text.send.get_secrets",
        return_value="example-text-api-key",
    ) as mock:
        yield mock


@fixture
def send_mock_2(get_text_secrets_mock):
    response = Response(
        200,
        json={
            "id": "1",
            "status": "sent"
        }
    )
    with respx.mock(base_url="https://t-e-x-t.example.com/") as mock:
        mock.post(name="send-text", url="send") % response
        yield mock


client = TestClient(app)


@fixture
def assert_all_mocked():
    with respx.mock(assert_all_called=True) as mock:
        yield mock


def test_waitlist_party_notification_update_given_added_to_waitlist_notification_update(
    assert_all_mocked, get_party_mock, send_mock_2
):
    response = client.post(
        "/waitlist/party/notification/update",
        json={
            "event_guid": "123",
            "party_guid": "456",
            "notification": "added_to_waitlist",
        },
    )
    
    send_mock_2.calls.assert_called_once()
    assert json.loads(send_mock_2.calls.last.request.content) == {"protocol": "sms", "to": "5555555551", "from": "55555555552", "message": "Welcome, we've added you to our waitlist. We expect to have your table prepared in about 30 minutes.",}
    assert response.json()["status"] == "sent"


# def test_waitlist_party_notification_update_given_table_prepared_notification_update(

# ):
#     response = _waitlist_party_notification_update(
#         NotificationUpdate(
#             event_guid="a", party_guid="b", notification="table_prepared"
#         )
#     )
#     send_mock.assert_called_once_with(
#         "sms",
#         "5555555551",
#         "5555555552",
#         "Hello, you're table is ready. To get seated please see the host.",
#     )
#     assert response.status == "sent"


# def test_waitlist_party_notification_update_given_waitlist_delayed_notification_update(

# ):
#     response = _waitlist_party_notification_update(
#         NotificationUpdate(
#             event_guid="a", party_guid="b", notification="waitlist_delayed"
#         )
#     )
#     send_mock.assert_called_once_with(
#         "sms",
#         "5555555551",
#         "5555555552",
#         "Apologies, it is taking longer than expected to finish preparing your table. Please see the host if you have any questions.",
#     )
#     assert response.status == "sent"
