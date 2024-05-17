def better_than_average(class_points, your_points):
    avarage = sum(class_points) / len(class_points)
    if avarage > your_points:
        return False
    return True


def test_better_than_average():
    assert better_than_average([2, 3], 5) == False
