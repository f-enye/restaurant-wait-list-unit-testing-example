import json
from datetime import datetime
from unittest.mock import patch

import respx
from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture

from unit_testing_disciplines.main import app


@fixture
def get_waitlist_api_key_mock():
    with patch(
        "unit_testing_disciplines.waitlists.parties.get_party.get_secret",
        return_value="example-waitlist-api-key",
    ) as mock:
        yield mock


@fixture
def get_party_mock(get_waitlist_api_key_mock):
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
def get_text_messages_api_key_mock():
    with patch(
        "unit_testing_disciplines.text_messages.send.get_secret",
        return_value="example-text-api-key",
    ) as mock:
        yield mock


@fixture
def send_mock(get_text_messages_api_key_mock):
    response = Response(200, json={"id": "1", "status": "sent"})
    with respx.mock(base_url="https://t-e-x-t.example.com/") as mock:
        mock.post(name="send-text", url="send") % response
        yield mock


client = TestClient(app)


def test_waitlist_party_notification_update_given_added_to_waitlist_notification_update(
    get_party_mock, send_mock
):
    response = client.post(
        "/waitlist/party/notification/update",
        json={
            "event_guid": "123",
            "party_guid": "456",
            "notification": "added_to_waitlist",
        },
    )

    send_mock.calls.assert_called_once()
    assert json.loads(send_mock.calls.last.request.content) == {
        "protocol": "sms",
        "to": "5555555551",
        "from": "5555555552",
        "message": "Welcome, we've added you to our waitlist. "
        "We expect to have your table prepared in about 30 minutes.",
    }
    assert response.json()["status"] == "sent"


def test_waitlist_party_notification_update_given_table_prepared_notification_update(
    get_party_mock, send_mock
):
    response = client.post(
        "/waitlist/party/notification/update",
        json={
            "event_guid": "123",
            "party_guid": "456",
            "notification": "table_prepared",
        },
    )
    send_mock.calls.assert_called_once()
    assert json.loads(send_mock.calls.last.request.content) == {
        "protocol": "sms",
        "to": "5555555551",
        "from": "5555555552",
        "message": "Hello, you're table is ready. To get seated please see the host.",
    }
    assert response.json()["status"] == "sent"


def test_waitlist_party_notification_update_given_waitlist_delayed_notification_update(
    get_party_mock, send_mock
):
    response = client.post(
        "/waitlist/party/notification/update",
        json={
            "event_guid": "123",
            "party_guid": "456",
            "notification": "waitlist_delayed",
        },
    )
    send_mock.calls.assert_called_once()
    assert json.loads(send_mock.calls.last.request.content) == {
        "protocol": "sms",
        "to": "5555555551",
        "from": "5555555552",
        "message": "Apologies, it is taking longer than expected to finish "
        "preparing your table. Please see the host if you have any questions.",
    }
    assert response.json()["status"] == "sent"
