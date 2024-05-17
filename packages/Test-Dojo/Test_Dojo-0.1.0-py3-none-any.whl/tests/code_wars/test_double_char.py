def double_char(s: str) -> str:
    return "".join(i * 2 for i in s)


def test_all_lower():
    assert double_char("String") == "SSttrriinngg"


def test_all_lower():
    assert double_char("Hello World") == "HHeelllloo  WWoorrlldd"
