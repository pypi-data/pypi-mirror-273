def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]


def test_is_palindrome():
    assert is_palindrome("a"), True
    assert is_palindrome("aba"), True
    assert is_palindrome("Abba"), True
    assert is_palindrome("malam"), True
    assert is_palindrome("walter"), False
    assert is_palindrome("kodok"), True
    assert is_palindrome("Kasue"), False
