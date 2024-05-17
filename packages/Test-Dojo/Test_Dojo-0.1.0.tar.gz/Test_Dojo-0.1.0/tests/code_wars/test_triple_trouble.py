def triple_trouble(one, two, three):
    result = ""
    for i in range(len(one)):
        result += one[i] + two[i] + three[i]
    return result


def test_triple_trouble():
    assert triple_trouble("aaa", "bbb", "ccc") == "abcabcabc"
    assert triple_trouble("toko", "didi", "biwi") == "tdboiikdwoii"


def test_1():
    assert triple_trouble("a", "b", "c") == "abc"


def test_2():
    assert triple_trouble("aa", "bb", "cc") == "abcabc"
