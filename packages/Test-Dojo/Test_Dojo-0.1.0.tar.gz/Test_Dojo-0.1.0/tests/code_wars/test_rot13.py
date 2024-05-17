import string

def rot13(message):
    rot_message = ""
    alphabet = dict(enumerate(list(string.ascii_letters)))
    alphabet_reverse = {
        value: key for key, value in alphabet.items()}
    alphabet_reverse[" "] = 1000
    alphabet[987] = " "

    for index, letter in enumerate(message):
        n = alphabet_reverse[letter] + 13
        if n > 25:
            n = n - 26
        if letter.isupper():
            rot_message = rot_message + message[index].replace(letter, alphabet[n]).upper()
        else:
            rot_message = rot_message + message[index].replace(letter, alphabet[n])

    return rot_message



    # alphabet = dict(enumerate(list(string.ascii_letters)))






def test_rot13():
    assert rot13("") == ""
    assert rot13(" ") == " "
    assert rot13("a") == "n"
    assert rot13("ab") == "no"
    assert rot13("abc") == "nop"
    assert rot13("abz") == "nom"
    assert rot13("Abz") == "Nom"
    assert rot13("Ab z") == "No m"
    assert rot13("aA bB zZ 1234 *!?%") == "nN oO mM 1234 *!?%"


