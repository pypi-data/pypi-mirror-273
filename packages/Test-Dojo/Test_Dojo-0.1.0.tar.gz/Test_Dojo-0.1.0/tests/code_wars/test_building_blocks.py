from dataclasses import dataclass


@dataclass
class Block:
    block: list

    def get_width(self):
        return self.block[0]

    def get_length(self):
        return self.block[1]

    def get_height(self):
        return self.block[2]

    def get_volume(self):
        return self.block[0] * self.block[1] * self.block[2]

    def get_surface_area(self):
        return (
            2 * (self.block[0] * self.block[1])
            + 2 * (self.block[1] * self.block[2])
            + 2 * (self.block[0] * self.block[2])
        )


def test_2_2_2():
    assert Block([2, 2, 2]).get_width() == 2
    assert Block([2, 2, 2]).get_length() == 2
    assert Block([2, 2, 2]).get_height() == 2
    assert Block([2, 2, 2]).get_volume() == 8
    assert Block([2, 2, 2]).get_surface_area() == 24
