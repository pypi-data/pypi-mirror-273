def alphanumeric(password):
    return password.isalnum()

    # if len(password) < 1:
    #     return False
    # for i in password:
    #     if i.isalpha() or i.isdigit():
    #         continue
    #     return False
    # return True


def test_alphanumeric():
    assert alphanumeric("") == False
    assert alphanumeric("a") == True
    assert alphanumeric("abd") == True
    assert alphanumeric("abd1") == True
    assert alphanumeric("abd1 ") == False
