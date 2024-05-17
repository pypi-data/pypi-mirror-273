def decimal_to_binary(decimal: int) -> str:
    binary = ""
    while decimal > 0:
        binary += str(decimal % 2)
        decimal //= 2
    return (16 - len(binary)) * "0" + binary[::-1]


def test_decimal_to_binary():
    assert decimal_to_binary(0) == "0000000000000000"
    assert decimal_to_binary(1) == "0000000000000001"
    assert decimal_to_binary(2) == "0000000000000010"
    assert decimal_to_binary(110) == "0000000001101110"
