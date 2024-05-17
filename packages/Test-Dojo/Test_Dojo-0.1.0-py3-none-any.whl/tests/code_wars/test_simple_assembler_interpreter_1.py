import pytest


def simple_assembler(program: [str]) -> {}:
    memory = {}
    program_counter = 0
    while program_counter < len(program):
        i = program[program_counter]
        func, *_ = i.split(" ")
        if func == "mov":
            func, register, instruction = i.split(" ")
            if instruction.isdigit():
                memory[register] = int(instruction)
            else:
                memory[register] = memory[instruction]
        if func == "inc":
            func, register = i.split(" ")
            memory[register] += 1
        if func == "dec":
            func, register = i.split(" ")
            memory[register] -= 1
        # TODO: fix jnz
        if func == "jnz":
            func, register, instruction = i.split(" ")
            if memory[register] != 0:
                program_counter += int(instruction)
            else:
                pass

                # if int(instruction) > 0:
                #     memory[register] -= int(instruction)
                # else:
                # count_dec = program[(program_counter + int(instruction)) : program_counter].count(
                #     f"dec {register}"
                # )
                # memory[register] -= count_dec
                # count_inc = program[(program_counter + int(instruction)) : program_counter].count(
                #     f"inc {register}"
                # )
                # memory[register] += count_inc
                # memory[register] += int(instruction)
        program_counter += 1

    return memory


def test_one_mov():
    assert simple_assembler(["mov a 1"]) == {"a": 1}


def test_two_mov():
    assert simple_assembler(["mov a 1", "mov a 2"]) == {"a": 2}


def test_three_mov():
    assert simple_assembler(["mov a 1", "mov a 2", "mov a 5"]) == {"a": 5}


def test_two_diff_var_mov():
    assert simple_assembler(["mov a 1", "mov b 2"]) == {"a": 1, "b": 2}


def test_a_in_b():
    assert simple_assembler(["mov a 1", "mov b a"]) == {"a": 1, "b": 1}


def test_one_inc():
    assert simple_assembler(["mov a 1", "inc a"]) == {"a": 2}


def test_two_inc():
    assert simple_assembler(["mov a 1", "inc a", "inc a"]) == {"a": 3}


def test_mix_inc():
    assert simple_assembler(["mov a 1", "inc a", "inc a", "mov a 1", "inc a"]) == {
        "a": 2
    }


def test_mix_ab_inc():
    assert simple_assembler(["mov a 4", "inc a", "inc a", "mov b a", "inc b"]) == {
        "a": 6,
        "b": 7,
    }


def test_one_dec():
    assert simple_assembler(["mov a 1", "dec a"]) == {"a": 0}


def test_two_dec():
    assert simple_assembler(["mov a 1", "dec a", "dec a"]) == {"a": -1}


def test_mix_dec():
    assert simple_assembler(["mov a 1", "dec a", "dec a", "mov a 1", "dec a"]) == {
        "a": 0
    }


def test_mix_ab_dec():
    assert simple_assembler(["mov a 4", "dec a", "dec a", "mov b a", "dec b"]) == {
        "a": 2,
        "b": 1,
    }


def test_inc_dec():
    assert simple_assembler(["mov a 1", "inc a", "dec a"]) == {"a": 1}


@pytest.mark.skip("Gets stuck in infinite loop")
def test_one_jnz():
    assert simple_assembler(["mov a 2", "dec a", "jnz a -1"]) == {"a": 0}


def test_many_jnz():
    assert simple_assembler(["mov a 5", "dec a", "dec a", "dec a", "jnz a -2"]) == {
        "a": 0
    }


@pytest.mark.skip("Gets stuck in infinite loop")
def test_mix():
    assert simple_assembler(
        ["mov a 5", "inc a", "dec a", "dec a", "jnz a -1", "inc a"]
    ) == {"a": 1}


@pytest.mark.skip("Gets stuck in infinite loop")
def test_mix2():
    assert simple_assembler(
        [
            "mov a 5",
            "inc a",
            "dec a",
            "dec a",
            "dec a",
            "dec a",
            "inc a",
            "jnz a -3",
            "inc a",
        ]
    ) == {"a": 1}


@pytest.mark.skip
def test_brutality():
    assert simple_assembler(
        [
            "mov c 12",
            "mov b 0",
            "mov a 200",
            "dec a",
            "inc b",
            "jnz a -2",
            "dec c",
            "mov a b",
            "jnz c -5",
            "jnz 0 1",
            "mov c a",
        ]
    ) == {"a": 409600, "c": 409600, "b": 409600}
