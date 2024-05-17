def validate_pin(pin):
    return pin.isdigit() and (len(pin) == 4 or len(pin) == 6)


def test_validate_pin():
    assert validate_pin("11111") == False
    assert validate_pin("1234") == True
    assert validate_pin("1111") == True
