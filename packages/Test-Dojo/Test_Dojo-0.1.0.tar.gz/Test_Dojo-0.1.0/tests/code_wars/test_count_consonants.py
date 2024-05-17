def consonant_count(s: str) -> int:
    return sum(
        1 for character in s.lower() if character.isalpha() and character not in "aeiou"
    )


def test_numbers():
    assert consonant_count("123") == 0


def test_vo2els():
    assert consonant_count("aeiou") == 0
