def mix(s1: str, s2: str) -> str:
    lst = []
    for i in range(97, 122):
        if s1.count(chr(i)) == s2.count(chr(i)) > 1:
            lst.append(f"=:{chr(i) * s2.count(chr(i))}")
        elif s1.count(chr(i)) > s2.count(chr(i)) and s1.count(chr(i)) > 1:
            lst.append(f"1:{chr(i)*s1.count(chr(i))}")
        elif s1.count(chr(i)) < s2.count(chr(i)) > 1:
            lst.append(f"2:{chr(i)*s2.count(chr(i))}")
    return "/".join(lst)


def test_1():
    assert mix("a", "b") == ""
    assert mix("aa", "bb") == "1:aa/2:bb"


def test_2():
    assert mix("aaab", "bbba") == "1:aaa/2:bbb"


def test_3():
    assert mix("aaabcc", "bbba") == "1:aaa/2:bbb/1:cc"


def test_4():
    assert mix("aaabccccc", "bbba") == "1:ccccc/1:aaa/2:bbb"


def test_5():
    assert mix("bbbaccccc", "aaab") == "1:ccccc/2:aaa/1:bbb"


def test_6():
    assert mix("ououou", "sssaa") == "1:ooo/2:sss/1:uuu/2:aa"


def test_7():
    assert mix("Are they here", "yes, they are here") == "2:eeeee/2:yy/=:hh/=:rr"
