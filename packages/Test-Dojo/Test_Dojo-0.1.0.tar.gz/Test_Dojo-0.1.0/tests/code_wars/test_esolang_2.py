def interpreter(code: str, tape: str) -> str:
    string = ""
    k = 0
    for i in code:
        if i == "*":
            if tape[k] == "0":
                string += "1"
            elif tape[k] == "1":
                string += "0"
            else:
                string += tape[k]
        if i == ">":
            string += tape[k]
        # TODO: '<' translate
        if i == "<":
            string -= tape[k]
        k += 1
    return string

    tape_list = [i for i in tape]
    program_counter = 0
    for i in code:
        if i == "*":
            if tape[program_counter] == "0":
                tape_list[program_counter] = "1"
            else:
                tape_list[program_counter] = "0"
        if i == ">":
            program_counter += 1
        if i == "<":
            program_counter -= 1
        if i == "[" and tape_list[program_counter] == "0":
            while i != "]":
                pass

    return "".join(tape_list)


def test_square_scope():
    assert interpreter(">>*[>*]>*", "10101010") == "10011010"


def test_mix_forward_mix_flip():
    assert interpreter(">>>>*>>*", "00101011") == "00100001"


def test_one_flip():
    assert interpreter("*", "0") == "1"


def test_one_forward_one_flip():
    assert interpreter(">*", "00") == "01"


def test_mix_forward_mix_flip():
    assert interpreter(">>>>*>>*", "00101011") == "00100010"


def test_one_backward_one_flip():
    assert interpreter(">*<", "010") == "000"


def test_one_backward_one_flip():
    assert interpreter(">*<", "010") == "000"


def test_many_forward_one_backward_one_flip():
    assert interpreter(">*>>><", "011010") == "001010"


def test_two_backwards():
    assert interpreter(">*>><<", "011010") == "001010"


def test_flip_after_backwards():
    assert interpreter(">>>>>*<*<<*", "00101100") == "00000000"
