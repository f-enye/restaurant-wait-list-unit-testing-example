from datetime import datetime
from unittest.mock import patch

from pytest import fixture

from restaurant_waitlist_notifier.main import (
    StatusUpdatedEventRequest,
    _waitlist_party_status_updated,
)
from restaurant_waitlist_notifier.text_messages.send import SendResult
from restaurant_waitlist_notifier.waitlists.parties.get_party import Party


@fixture
def get_party_mock():
    with patch(
        "restaurant_waitlist_notifier.main.get_party",
        return_value=Party(
            name="Peter",
            phone_number="5555555551",
            size=1,
            time_of_arrival=datetime(2024, 1, 1, 1, 0),
            quoted_time_in_minutes=30,
        ),
    ) as mock:
        yield mock


@fixture
def send_mock():
    with patch(
        "restaurant_waitlist_notifier.main.send",
        return_value=SendResult(id="1", status="sent"),
    ) as mock:
        yield mock


def test_status_updated_to_added_to_waitlist(get_party_mock, send_mock):
    response = _waitlist_party_status_updated(
        StatusUpdatedEventRequest(
            event_id="test-event-uuid",
            party_id="test-party-uuid",
            status="added_to_waitlist",
        )
    )
    send_mock.assert_called_once_with(
        "sms",
        "5555555551",
        "Welcome, we've added you to our waitlist. "
        "We expect to have your table prepared in about 30 minutes.",
    )
    assert response.status == "sent"


def test_status_updated_to_table_prepared(get_party_mock, send_mock):
    response = _waitlist_party_status_updated(
        StatusUpdatedEventRequest(
            event_id="test-event-uuid",
            party_id="test-party-uuid",
            status="table_prepared",
        )
    )
    send_mock.assert_called_once_with(
        "sms",
        "5555555551",
        "Hello, you're table is ready. To get seated please see the host.",
    )
    assert response.status == "sent"


def test_status_updated_to_waitlist_deplayed(get_party_mock, send_mock):
    response = _waitlist_party_status_updated(
        StatusUpdatedEventRequest(
            event_id="test-event-uuid",
            party_id="test-party-uuid",
            status="waitlist_delayed",
        )
    )
    send_mock.assert_called_once_with(
        "sms",
        "5555555551",
        "Apologies, it is taking longer than expected to finish preparing your "
        "table. Please see the host if you have any questions.",
    )
    assert response.status == "sent"
