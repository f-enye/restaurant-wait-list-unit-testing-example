from unittest.mock import patch, ANY
from pytest import fixture
from unit_testing_disciplines.external.text.send import SendResult
from unit_testing_disciplines.main import Body, send_text

@fixture
def send_mock():
    with patch("unit_testing_disciplines.main.send", return_value=SendResult(id="1", status="sent")) as mock:
        yield mock



def test_main_given_text_is_sent_successfully(send_mock):
    response = send_text(Body(eventGuid="a", partyGuid="b", notification="added-to-waitlist"))
    send_mock.assert_called_once_with(ANY, "sms", "5555555551", "5555555552", "Hello")
    assert response.status == "sent"
