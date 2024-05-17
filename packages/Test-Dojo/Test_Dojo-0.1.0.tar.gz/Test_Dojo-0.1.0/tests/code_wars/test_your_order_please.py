def order(sentence):
    sen = [""] * (sentence.count(" ") + 1)
    for word in sentence.split():
        for character in word:
            if character.isdigit():
                sen[int(character) - 1] = word
    return " ".join(sen)


def test_order():
    assert order("is2 Thi1s T4est 3a") == "Thi1s is2 3a T4est"
