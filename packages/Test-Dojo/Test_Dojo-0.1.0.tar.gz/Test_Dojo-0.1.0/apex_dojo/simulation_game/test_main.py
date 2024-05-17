from random import randint

import pytest

from apex_dojo.simulation_game.tdd_main import Creature


def test_start_location(predator: Creature, pray: Creature):
    predator.location = 0
    pray.location = randint(0, 10)

    assert predator.location, pray.location
