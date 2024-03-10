from unittest.mock import patch
from pytest import fixture
from unit_testing_disciplines.main import Body, send_text, SendResult

@fixture
def send_mock():
    with patch("unit_testing_disciplines.main.send", return_value=SendResult(id="1", status="sent")):
        yield



def test_main(send_mock):
    response = send_text(Body(from_="5555555555", to="5555555551", text="hello"))
    assert response.status == "sent"
