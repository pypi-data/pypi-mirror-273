from collections import Counter


def top_3_words(text: str) -> list:
    contains_alphabet = any(i.isalpha() for i in text)
    text = "".join(
        [
            i
            if ord(i) == 32 or ord(i) == 39 or 90 >= ord(i) >= 65 or 122 >= ord(i) >= 97
            else " "
            for i in text.lower()
        ]
    ).split()
    return [i[0] for i in Counter(text).most_common(3)] if contains_alphabet else []


def test_():
    assert top_3_words("a b b c c c d d d d") == ["d", "c", "b"]


def test_non_asc():
    assert top_3_words("  //wont won't won't ") == ["won't", "wont"]


def test_no_words():
    assert top_3_words("  '''  ") == []
