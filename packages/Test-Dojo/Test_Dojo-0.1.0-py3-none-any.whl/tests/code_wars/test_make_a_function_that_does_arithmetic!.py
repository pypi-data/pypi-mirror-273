def arithmetic(a: int, b: int, operator: str) -> float:
    if operator == "add":
        return a + b
    if operator == "subtract":
        return a - b
    if operator == "multiply":
        return a * b
    else:
        return a / b


def test_arithmetic():
    assert arithmetic(1, 2, "add") == 3
    assert arithmetic(5, 7, "add") == 12
    assert arithmetic(8, 2, "subtract") == 6
    assert arithmetic(8, 2, "multiply") == 16
    assert arithmetic(8, 2, "devide") == 4
