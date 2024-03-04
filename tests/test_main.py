from unit_testing_disciplines.main import Body, send_text


def test_main():
    response = send_text(Body(text="hello"))
    assert response["body"].text == "hello"
