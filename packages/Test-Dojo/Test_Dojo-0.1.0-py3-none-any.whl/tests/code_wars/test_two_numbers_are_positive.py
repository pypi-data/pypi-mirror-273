def two_are_positive(a, b, c):
    if a > 0 and b > 0 and c > 0:
        return False
    if (a > 0 and b > 0) or (a > 0 and c > 0) or (b > 0 and c > 0):
        return True
    return False

# best practice
# def two_are_positive(a, b, c):
#     return sum([a>0, b>0, c>0]) == 2

def test_1():
    assert two_are_positive(-4, 6, 0) == False

def test_2():
    assert two_are_positive(4, 6, 8) == False