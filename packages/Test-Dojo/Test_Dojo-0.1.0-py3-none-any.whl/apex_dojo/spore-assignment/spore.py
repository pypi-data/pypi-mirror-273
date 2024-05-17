from __future__ import annotations

from dataclasses import dataclass, field
from random import randint

maximum_stamina = 100

MOVEMENT_COST = {
    "crawl": 1,
    "hop": 2,
    "walk": 2,
    "run": 4,
    "fly": 4,
}

MOVEMENT_SPEED = {
    "crawl": 1,
    "hop": 3,
    "walk": 4,
    "run": 6,
    "fly": 8,
}


@dataclass
class Creature:
    location: int = 0
    stamina: int = 0
    first_leg: bool = False
    second_leg: bool = False
    wings: bool = False
    abilities: list = field(default_factory=list)

    def spawn_creature(self, location) -> dict[str:int]:
        self.location = location
        self.stamina = randint(1, maximum_stamina)

    def evolve_creature(self):
        if self.stamina > 20:
            self.first_leg = True
        if self.stamina > 40:
            self.second_leg = True
        if self.stamina > 80:
            self.wings = True

    def available_abilities(self):
        if not self.first_leg:
            self.abilities.append("crawl")
        if self.first_leg:
            self.abilities.append("crawl")
            self.abilities.append("hop")
        if self.second_leg:
            self.abilities.append("walk")
            self.abilities.append("run")
        if self.wings:
            self.abilities.append("fly")

    def move(self, movement):
        if self.check_stamina_for_ability(movement):
            self.location += MOVEMENT_SPEED[movement]
            self.stamina -= MOVEMENT_COST[movement]
            print(
                f"predator used: {movement}, moved by: {MOVEMENT_SPEED[movement]}, used stamina: {MOVEMENT_COST[movement]}"
            )

    def check_stamina_for_ability(self, movement):
        return not MOVEMENT_COST[movement] > self.stamina


predator = Creature()
predator.spawn_creature(0)
predator.evolve_creature()
predator.available_abilities()

pray = Creature()
pray.spawn_creature(randint(1, 1000))
pray.evolve_creature()
pray.available_abilities()

distance_between = pray.location - predator.location
print(f"Predator: {predator}")
print(f"Pray: {pray}")

print(
    f"predator location: {predator.location} - stamina: {predator.stamina} - distance: {distance_between}"
)
for i in range(100):
    last_ability = predator.abilities[-1]
    predator.move(last_ability)
    distance_between = pray.location - predator.location
    print(
        f"{i}) predator location: {predator.location} - stamina: {predator.stamina} - distance: {distance_between}"
    )
    if distance_between <= 0:
        print(f"{i}) REEEEEEEEEEEEEE$#%^*%*$&#$!!!")
        break
    if not predator.stamina:
        print(f"{i}) Exhausted")
        break

    # if (
    #     distance_between in list(MOVEMENT_SPEED.values())
    #     and list(MOVEMENT_SPEED.keys())[
    #         list(MOVEMENT_SPEED.values()).index(distance_between)
    #     ]
    #     in predator.abilities
    # ):
    #     movement = list(MOVEMENT_SPEED.keys())[
    #         list(MOVEMENT_SPEED.values()).index(distance_between)
    #     ]
    #     print(
    #         f"predator location: {predator.location} - stamina: {predator.stamina} - distance: {distance_between}"
    #     )
    #     predator.location += MOVEMENT_SPEED[movement]
    #     predator.stamina -= MOVEMENT_COST[movement]
    #     distance_between = pray.location - predator.location
    #     print(
    #         f"predator used: {movement}, moved by: {MOVEMENT_SPEED[movement]}, used stamina: {MOVEMENT_COST[movement]}"
    #     )
    #     print(
    #         f"predator location: {predator.location} - stamina: {predator.stamina} - distance: {distance_between}"
    #     )
    #     if predator.location == pray.location:
    #         print("REEEEEEEEEEEEEE$#%^*%*$&#$!!!")
    #         break
    # else:
    #     movement = predator.abilities[-1]
    #     if predator.check_stamina_for_ability(MOVEMENT_COST[movement]):
    #         predator.location += MOVEMENT_SPEED[movement]
    #         predator.stamina -= MOVEMENT_COST[movement]
    #         distance_between = pray.location - predator.location
    #         print(
    #             f"predator used: {movement}, moved by: {MOVEMENT_SPEED[movement]}, used stamina: {MOVEMENT_COST[movement]}"
    #         )
    #         print(
    #             f"predator location: {predator.location} - stamina: {predator.stamina} - distance: {distance_between}"
    #         )


# list(MOVEMENT_COST.keys())[list(MOVEMENT_COST.values()).index(16)]
