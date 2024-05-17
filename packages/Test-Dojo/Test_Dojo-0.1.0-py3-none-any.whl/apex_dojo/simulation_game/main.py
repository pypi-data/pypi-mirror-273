from dataclasses import dataclass
from random import randint, choice


@dataclass
class Creature:
    location: int
    claws: str
    teeth: int

    legs: int = randint(0, 2)
    wings: int = randint(0, 4)
    stamina: int = 100
    health: int = 100

    def move(self, stamina, location):
        self.stamina -= stamina
        self.location += location

    def attack(self, enemy):
        if self.stamina >= 2:
            damage_multiplier = {"Small": 2, "Medium": 3, "Big": 4}.get(self.claws, 1)
            self.stamina -= 2
            enemy.health -= 5 * damage_multiplier
        else:
            self.stamina -= 2
            enemy.health -= 5

    def crawl(self):
        if self.stamina > 0:
            self.move(1, 1)
        else:
            self.evolve()

    def hop(self):
        if self.legs >= 1 and self.stamina >= 20:
            self.move(2, 3)
        else:
            self.evolve()

    def walk(self):
        if self.legs >= 2 and self.stamina >= 40:
            self.move(2, 4)
        else:
            self.evolve()

    def run(self):
        if self.legs >= 2 and self.stamina >= 60:
            self.move(4, 6)
        else:
            self.evolve()

    def fly(self):
        if self.wings >= 2 and self.stamina >= 80:
            self.move(4, 8)
        else:
            self.evolve()

    def evolve(self, is_fight_phase=False):
        if not is_fight_phase:
            self.legs += 1
            self.wings += 1
            print(
                f"{self.__class__.__name__} evolved: Legs: {self.legs}, Wings: {self.wings}"
            )


def randomize_creature_actions():
    return choice(
        [
            method
            for method in dir(Creature)
            if callable(getattr(Creature, method))
            and not method.startswith("__")
            and method not in ("move", "attack", "evolve")
        ]
    )


def print_creature_info(print_creature, print_name):
    print(f"{print_name} Characteristics:")
    print(
        f"Location: {print_creature.location} Legs: {print_creature.legs} Claws: {print_creature.claws}"
    )
    print(
        f"Stamina: {print_creature.stamina} Teeth: {print_creature.teeth} Health: {print_creature.health}"
    )
    print(f"Wings: {print_creature.wings} \n")


predator = Creature(location=0, claws=choice(["Small", "Medium", "Big"]), teeth=1)
pray = Creature(
    location=randint(0, 10), claws=choice(["Small", "Medium", "Big"]), teeth=1
)

creatures = [predator, pray]
creature_names = ["Predator", "Pray"]

for creature, name in zip(creatures, creature_names):
    action = randomize_creature_actions()
    action_result = getattr(creature, action)()

    print(f"Method called for {name}:", action)
    print_creature_info(creature, name)

if predator.stamina == 0:
    print("Pray ran into infinity")


def should_start_fight(creature_1, creature_2):
    return creature_1.location >= creature_2.location and creature_1.stamina > 0


fight_phase_started = False

while not fight_phase_started:
    for creature, name in zip(creatures, creature_names):
        action = randomize_creature_actions()
        action_result = getattr(creature, action)()

        print(f"Method called for {name}:", action)
        print_creature_info(creature, name)

        fight_phase_started = should_start_fight(predator, pray)

        if any(creature.stamina <= 0 for creature in creatures):
            break

if predator.location >= pray.location:
    print("Fight Phase")

    round_counter = 0

    while (
        predator.health > 0
        and pray.health > 0
        and predator.stamina > 0
        and pray.stamina > 0
    ):
        round_counter += 1
        print(f"Round: {round_counter}")

        if predator.stamina > pray.stamina:
            predator.attack(pray)
            pray.attack(predator)
        else:
            pray.attack(predator)
            predator.attack(pray)

        print_creature_info(predator, "Predator")
        print_creature_info(pray, "Pray")

        if pray.health <= 0:
            print("Pray has been defeated!")
            break

        if predator.health <= 0:
            print("Pray ran into infinity")
            break
