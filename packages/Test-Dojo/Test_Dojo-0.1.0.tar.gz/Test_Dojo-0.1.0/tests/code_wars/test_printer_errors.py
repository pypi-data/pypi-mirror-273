def printer_error(s):
    lst = ""
    for j in range(ord("n"), ord("z") + 1):
        if chr(j) in s:
            lst += chr(j) * s.count(chr(j))
    return f"{len(lst)}/{len(s)}"


def test_1():
    assert printer_error("aao") == "1/3"
