def duplicate_encode(word: str) -> str:
    word = word.lower()
    new_str = ""
    for i in word:
        if word.count(i) < 2:
            new_str += "("
        else:
            new_str += ")"
    return new_str


def test_no_dups():
    assert duplicate_encode("din") == "((("


def test_some_dups():
    assert duplicate_encode("recede") == "()()()"


def test_upper_case():
    assert duplicate_encode("Success") == ")())())"


def test_complicated():
    assert duplicate_encode("@OrWs(PbE)dBJjgpN()e)") == "((((()))))()))()())))"
