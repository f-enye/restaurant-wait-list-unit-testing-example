from unit_testing_disciplines.main import Body, send_text


def test_main():
    assert send_text(Body(text="hello"))
