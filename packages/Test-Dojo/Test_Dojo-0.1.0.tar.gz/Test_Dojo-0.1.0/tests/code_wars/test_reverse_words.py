def reverse_words(text: str) -> str:
    return " ".join(i[::-1] for i in text.split(" "))


def test_one():
    assert reverse_words("ab") == "ba"


def test_two_same():
    assert reverse_words("ab ab") == "ba ba"


def test_two_different():
    assert reverse_words("my name") == "ym eman"


def test_mix():
    assert (
        reverse_words("The quick brown fox jumps over the lazy dog.")
        == "ehT kciuq nworb xof spmuj revo eht yzal .god"
    )


def test_double_space():
    assert reverse_words("double  spaced  words") == "elbuod  decaps  sdrow"
