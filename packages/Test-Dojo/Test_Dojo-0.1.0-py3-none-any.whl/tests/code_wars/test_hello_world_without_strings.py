def hello_world():
    return (
        chr(ord("H"))
        + chr(ord("e"))
        + 2 * chr(ord("l"))
        + chr(ord("o"))
        + chr(ord(","))
        + chr(ord(" "))
        + chr(ord("W"))
        + chr(ord("o"))
        + chr(ord("r"))
        + chr(ord("l"))
        + chr(ord("d"))
        + chr(ord("!"))
    )


def test_hello_world():
    assert hello_world() == "Hello, World!"
