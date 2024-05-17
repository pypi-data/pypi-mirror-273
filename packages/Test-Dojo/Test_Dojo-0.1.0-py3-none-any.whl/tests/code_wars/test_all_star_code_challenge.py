def str_count(strng, letter):
    lst = []
    for i in strng:
        if i == letter:
            lst.append(i)
    return len(lst)

def test_1():
    assert str_count("letter", "t") == 2