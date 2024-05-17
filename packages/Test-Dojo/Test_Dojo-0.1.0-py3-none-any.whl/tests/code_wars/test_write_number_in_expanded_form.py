def expanded_form(num: int) -> str:
    return " + ".join(
        str(num)[i] + "0" * (len(str(num)) - i - 1)
        for i in range(len(str(num)))
        if str(num)[i] != "0"
    )


def expanded_form(num):
    return " + ".join(
        i + "0" * (len(str(num)) - j - 1) for j, i in enumerate(str(num)) if i != "0"
    )


def test_single():
    assert expanded_form(1) == "1"


def test_double():
    assert expanded_form(12) == "10 + 2"


def test_four():
    assert expanded_form(70304) == "70000 + 300 + 4"
