import math
from dataclasses import dataclass


@dataclass
class Sphere(object):
    radius: int
    mass: int

    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass

    def get_volume(self):
        return round(4 / 3 * math.pi * self.radius**3, 5)

    def get_surface_area(self):
        return round(4 * math.pi * self.radius**2, 5)

    def get_density(self):
        return round(self.get_mass() / (4 / 3 * math.pi * self.radius**3), 5)


def test_sphere_2_50():
    assert Sphere(2, 50).get_radius() == 2
    assert Sphere(2, 50).get_mass() == 50
    assert Sphere(2, 50).get_volume() == 33.51032
    assert Sphere(2, 50).get_surface_area() == 50.26548
    assert Sphere(2, 50).get_density() == 1.49208
