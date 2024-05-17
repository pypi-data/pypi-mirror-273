import copy
import random


class Hat:
    def __init__(self, **kwargs: int):
        self.contents = [key for key in kwargs.keys() for _ in range(kwargs[key])]

    def draw(self, number: int) -> list[str]:
        drawn_balls = []

        if number > len(self.contents):
            return self.contents

        for i in range(number):
            drawn_balls.append(random.choice(self.contents))
            self.contents.remove(drawn_balls[-1])

        return drawn_balls


def experiment(
    hat: Hat, expected_balls: dict[str, int], num_balls_drawn: int, num_experiments: int
) -> float | int:
    success = 0

    for i in range(num_experiments):
        drawn_balls = copy.deepcopy(hat).draw(num_balls_drawn)
        expected_balls_copy = copy.deepcopy(expected_balls)

        for color in drawn_balls:
            if color in expected_balls_copy:
                expected_balls_copy[color] -= 1

        if all(value <= 0 for value in expected_balls_copy.values()):
            success += 1

    probability = success / num_experiments

    return probability
