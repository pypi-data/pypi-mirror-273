def duplicate_count(text):
    duplicate_num = []
    for letter in text.lower():
        if text.lower().count(letter) > 1 and letter not in duplicate_num:
            duplicate_num.append(letter)
    return len(duplicate_num)


def test_duplicates():
    assert duplicate_count("") == 0
    assert duplicate_count("a") == 0
    assert duplicate_count("ab") == 0
    assert duplicate_count("aba") == 1
    assert duplicate_count("abaa") == 1
    assert duplicate_count("abab") == 2
    assert duplicate_count("abaB") == 2
    assert duplicate_count("abaB11") == 3
