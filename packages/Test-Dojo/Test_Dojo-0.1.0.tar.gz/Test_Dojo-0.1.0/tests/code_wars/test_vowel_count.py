# Variant 1
# def get_count(sentence):
#     count = 0
#     for i in sentence:
#         if i == "a" or i == "e" or i == "i" or i == "o" or i == "u":
#             count += 1
#     return count


# Variant 2
# def get_count(sentence):
#     vowel_count = 0
#     vowels = ["a", "e", "i", "o", "u"]
#     for char in sentence:
#         if char in vowels:
#             vowel_count += 1
#     return vowel_count


# Variant 3
def get_count(sentence):
    vowels = ["a", "e", "i", "o", "u"]
    count = len([char for char in sentence if char in vowels])
    return count


def test_get_count():
    assert get_count("aeiou") == 5
