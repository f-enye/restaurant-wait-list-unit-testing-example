from datetime import datetime
from unittest.mock import patch, ANY
from pytest import fixture
from unit_testing_disciplines.external.text.send import SendResult
from unit_testing_disciplines.external.waitlist.party.party_information import Party
from unit_testing_disciplines.main import Body, waitlist_party_notification_update


@fixture
def send_mock():
    with patch(
        "unit_testing_disciplines.main.send",
        return_value=SendResult(id="1", status="sent"),
    ) as mock:
        yield mock


@fixture
def get_party_mock():
    with patch(
        "unit_testing_disciplines.main.get_party",
        return_value=Party(
            name="Peter",
            phone_number="5555555551",
            size=1,
            time_of_arrival=datetime(2024, 1, 1, 1, 0),
            quoted_time_in_minutes=30,
        ),
    ) as mock:
        yield mock


def test_waitlist_party_notification_update_given_added_to_waitlist_notification_update(
    get_party_mock, send_mock
):
    response = waitlist_party_notification_update(
        Body(event_guid="a", party_guid="b", notification="added_to_waitlist")
    )
    send_mock.assert_called_once_with(
        ANY,
        "sms",
        "5555555551",
        "5555555552",
        "Welcome, we've added you to our waitlist. We expect to have your table prepared in about 30 minutes.",
    )
    assert response.status == "sent"


def test_waitlist_party_notification_update_given_table_prepared_notification_update(
    get_party_mock, send_mock
):
    response = waitlist_party_notification_update(
        Body(event_guid="a", party_guid="b", notification="table_prepared")
    )
    send_mock.assert_called_once_with(
        ANY,
        "sms",
        "5555555551",
        "5555555552",
        "Hello, you're table is ready. To get seated please see the host.",
    )
    assert response.status == "sent"


def test_waitlist_party_notification_update_given_waitlist_delayed_notification_update(
    get_party_mock, send_mock
):
    response = waitlist_party_notification_update(
        Body(event_guid="a", party_guid="b", notification="waitlist_delayed")
    )
    send_mock.assert_called_once_with(
        ANY,
        "sms",
        "5555555551",
        "5555555552",
        "Apologies, it is taking longer than expected to finish preparing your table. Please see the host if you have any questions.",
    )
    assert response.status == "sent"
