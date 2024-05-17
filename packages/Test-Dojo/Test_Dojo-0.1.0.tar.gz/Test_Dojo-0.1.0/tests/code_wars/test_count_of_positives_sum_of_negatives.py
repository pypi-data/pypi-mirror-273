def count_positives_sum_negatives(arr):
    list_count = [i for i in arr if i > 0]
    list_sum = [j for j in arr if j < 0]
    return [len(list_count), sum(list_sum)] if arr else []


def test_count_positives_sum_negatives():
    assert count_positives_sum_negatives(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, -11, -12, -13, -14, -15]
    ) == [10, -65]
