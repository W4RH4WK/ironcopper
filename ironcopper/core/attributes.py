"""
# Attributes

Attributes model character's inherent characteristics.
They determine stats like a characters physical strength or how attractive they are.
"""

from typing import Optional, Tuple
from .checks import Outcome, check, extendedCheck


class Attribute:
    """
    Each attribute is a numeric value, usually between 1 and 20, where 8 corresponds to the human average.

    Instance variables:
    - `.score`
    """

    def __init__(self, score, label):
        self.score = score
        self.label = label

    def modifier(self):
        """
        Checks are commonly done in combination with a given attribute or skill.
        Either way, an **attribute modifier**, calculated as `score - 10` is subtracted from the threshold.

        `new_threshold = old_threshold - (score - 10)`
        """
        return self.score - 10

    def check(self, threshold: int, adv: int = 0) -> Outcome:
        if verboseAttributeChecks:
            print(f'{self.label} modifier: {self.modifier()}')

        return check(threshold - self.modifier(), adv)

    def extendedCheck(self, threshold: int, maxRolls: Optional[int] = None) -> Tuple[Outcome, int]:
        if verboseAttributeChecks:
            print(f'{self.label} modifier: {self.modifier()}')

        return extendedCheck(threshold - self.modifier(), maxRolls)

    def __str__(self):
        return f'{self.label}: {self.score}'


class Strength(Attribute):
    """
    Strength is the main melee attribute and determines the raw, physical power of your character.
    A stronger character can lift heavier objects and throw objects further.
    Note that the a characters endurance is not determined by the strength attribute.
    """

    def __init__(self, score):
        super(Strength, self).__init__(score, 'Str')


class Dexterity(Attribute):
    """
    Dexterity determines a character's fine motor skills and agility.
    This is your main firearms attribute, but is also used for actions where a character has to carefully control their body.
    """

    def __init__(self, score):
        super(Dexterity, self).__init__(score, 'Dex')


class Constitution(Attribute):
    """
    Constitution governs a character's health and resistances.
    A higher constitution improves the survivability of the character.
    """

    def __init__(self, score):
        super(Constitution, self).__init__(score, 'Con')


class Intelligence(Attribute):
    """
    Intelligence is the main hacking attribute and used for all actions that require direct interaction with technology.
    """

    def __init__(self, score):
        super(Intelligence, self).__init__(score, 'Int')


class Wisdom(Attribute):
    """
    The wisdom attribute is the main defense attribute and corresponds to a characters situational awareness.
    """

    def __init__(self, score):
        super(Wisdom, self).__init__(score, 'Wis')


class Charisma(Attribute):
    """
    Note only does charisma determine how attractive your character is, it is also the attribute used for social related actions.
    """

    def __init__(self, score):
        super(Charisma, self).__init__(score, 'Cha')


verboseAttributeChecks = True
"""Enabling this option shows attribute modifiers for checks."""
