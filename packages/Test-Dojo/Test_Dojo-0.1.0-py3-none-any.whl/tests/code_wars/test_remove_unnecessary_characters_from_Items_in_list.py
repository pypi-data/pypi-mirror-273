import re


def remove_char(array: list) -> list:
    lst = []
    for i in array:
        non_decimal = re.compile(r"[^\d.]+")
        # num = re.sub("\.+", ".", non_decimal[0])
        # lst.append(num.sub("", i).strip("."))
    return non_decimal


def test_1():
    assert remove_char(["@43.12"]) == ["43.12"]


def test_2():
    assert remove_char(["@2&.33"]) == ["2.33"]


def test_3():
    assert remove_char(["@22521&..33"]) == ["22521.33"]


def test_3():
    assert remove_char(["..@22521&..33.."]) == ["22521.33"]
