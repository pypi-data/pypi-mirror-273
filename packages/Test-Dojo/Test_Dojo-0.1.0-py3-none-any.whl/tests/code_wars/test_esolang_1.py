def my_first_interpreter(code: str) -> str:
    code_to_list = [i for i in code]
    counter = 0
    string = ""
    for i in code_to_list:
        if i == "+":
            counter += 1
            if counter == 256:
                counter = 0
        elif i == ".":
            string += chr(counter)
    return string


def test_uppercase():
    assert my_first_interpreter("+" * 65 + ".") == "A"
    assert my_first_interpreter("+" * 65 + ".+.") == "AB"


def test_comma():
    assert my_first_interpreter("+" * 44 + ".") == ","


def test_previous():
    assert my_first_interpreter("+" * 66 + "." + "+" * 190 + "+" * 65 + ".") == "BA"
