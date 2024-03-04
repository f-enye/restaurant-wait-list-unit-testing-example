from unit_testing_disciplines.main import Body, send_text


def test_main():
    response = send_text(Body(from_="5555555555", to="5555555551", text="hello"))
    assert response["body"].text == "hello"
