def better_than_average(class_points, your_points):
    return your_points > sum(class_points) / len(class_points)


def test_better_than_average():
    assert better_than_average([2, 3], 5) == True
