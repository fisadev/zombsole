# coding: utf-8
from zombsole.core import Weapon


def _new_weapon_class(name, max_range, damage_range):
    """Create new weapon class."""
    class NewWeapon(Weapon):
        def __init__(self):
            super(NewWeapon, self).__init__(name,
                                            max_range,
                                            damage_range)

    NewWeapon.__name__ = name
    return NewWeapon


ZombieClaws = _new_weapon_class('ZombieClaws', 1.5, (5, 10))

Knife = _new_weapon_class('Knife', 1.5, (5, 10))
Axe = _new_weapon_class('Axe', 1.5, (75, 100))

Gun = _new_weapon_class('Gun', 6, (10, 50))
Rifle = _new_weapon_class('Rifle', 10, (25, 75))
Shotgun = _new_weapon_class('Shotgun', 3, (75, 100))
