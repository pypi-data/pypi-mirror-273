def transpose_two_strings(arr):
    string1, string2 = arr[0], arr[1]
    max_length = max(len(string1), len(string2))
    transposed = []

    for i in range(max_length):
        char1 = string1[i] if i < len(string1) else " "
        char2 = string2[i] if i < len(string2) else " "
        transposed.append(char1 + " " + char2)

    return "\n".join(transposed)


def test_transpose_two_strings():
    assert transpose_two_strings(["Hi", "No"]) == "H N\ni o"
    assert transpose_two_strings(["Buy", "Yes"]) == "B Y\nu e\ny s"
