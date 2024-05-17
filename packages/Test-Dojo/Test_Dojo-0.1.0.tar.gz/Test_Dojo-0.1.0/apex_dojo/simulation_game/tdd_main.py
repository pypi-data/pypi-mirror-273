from dataclasses import dataclass
from random import randint


@dataclass
class Creature:
    location: int
    claws: str
    teeth: int

    legs: int = randint(0, 2)
    wings: int = randint(0, 4)
    stamina: int = 100
    health: int = 100
