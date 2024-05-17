def encryptor(key: int, message: str) -> str:
    message = [ord(i) for i in message]

    lst = []

    for character_ord in message:
        if 96 < character_ord < 123 or 64 < character_ord < 91:
            for k in range(max(key, -key)):
                if key > 0:
                    character_ord += 1
                else:
                    character_ord += -1

                if character_ord == 123:
                    character_ord = 97
                if character_ord == 91:
                    character_ord = 65
                if character_ord == 96:
                    character_ord = 122
                if character_ord == 64:
                    character_ord = 90
        lst.append(chr(character_ord))

    return "".join(lst)


def test_1():
    assert encryptor(1, "") == ""


def test_2():
    assert encryptor(1, "a") == "b"


def test_3():
    assert encryptor(1, "ab") == "bc"
    assert encryptor(1, "ab") == "bc"


def test_4():
    assert encryptor(1, "z") == "a"


def test_5():
    assert encryptor(1, "A") == "B"


def test_6():
    assert encryptor(-5, "Hello World!") == "Czggj Rjmgy!"
