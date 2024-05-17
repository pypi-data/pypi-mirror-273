def capital_indexes(input_string: str) -> list:
    return [i for i, char in enumerate(input_string) if char.isupper()]


def test_capital_indexes():
    assert capital_indexes("") == []
    assert capital_indexes("HeLlO") == [0, 2, 4]
    assert capital_indexes("ZaZZs") == [0, 2, 3]
