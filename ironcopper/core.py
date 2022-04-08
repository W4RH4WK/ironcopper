"""
# Core Mechanics

Iron & Copper, like any good pen-and-paper RPG uses dice to determine the outcome of actions.
There are only 3 basic types of rolls that are used for all mechanics of the game:

- **Skill checks** determine whether an action succeeds or fails.
- **Extended skill checks** determine how long an action takes.
  Failure happens in case there is a timelimit, which is exceeded.
- **Damage rolls** determine how much damage an offensive action inflicts.
  Note that not all offensive actions rely on damage rolls.

"""

import random

from enum import Enum
from typing import Optional, Tuple


def d20(adv: int = 0) -> int:
    """
    Rolls a 20-sided die (D20) and returns the result — the higher, the better.
    This is commonly used for skill checks and extended skill checks.

    There is a twist though:
    - With **advantage**, multiple dice are rolled, the result is determined by the highest die.
    - **Disadvantage** works the same, but the lowest die determines the result.

    `abs(adv)` determines the number of dice added, a positive or negative value indicates advantage or disadvantage respectively.
    Advantage and disadvantage on the same roll cancel each other out.

    Example:
    ```
    > d20()             # a regular roll
    D20: 5

    > d20(-1)           # roll with disadvantage
    D20-: [19, 3] → 3

    > d20(2)            # roll with double advantage
    D20+: [9, 4, 16] → 16
    ```
    """

    rolls = [random.randint(1, 20) for _ in range(abs(adv) + 1)]

    if adv > 0:
        result = max(rolls)
    else:
        result = min(rolls)

    if verboseRolls:
        if adv != 0:
            print(f'{_d20label(adv)}: {rolls} → {result}')
        else:
            print(f'{_d20label(adv)}: {result}')

    return result


def _d20label(adv: int = 0) -> str:
    label = 'D20'
    if adv > 0:
        label += '+'
    elif adv < 0:
        label += '-'
    return label


def d6(count: int = 1, critical: bool = False) -> int:
    """
    Rolls 6-sided dice (D6), commonly used for damage rolls.
    The result is simply the sum of all dice.

    Like with the 20-sided role, there is a twist.
    If a damage roll is a **critical damage roll**, the result is increased by `6 * count`.

    Example:
    ```
    > d6(2)             # a regular roll
    2D6: [2, 5] → 7

    > d6(3, critical=True)
    3D6+: [1, 3, 1] → 23
    ```
    """

    rolls = [random.randint(1, 6) for _ in range(count)]
    result = sum(rolls)

    if critical:
        result += count * 6

    if verboseRolls:
        if count > 1:
            print(f'{_d6label(count=count, critical=critical)}: {rolls} → {result}')
        else:
            print(f'{_d6label(count=count, critical=critical)}: {result}')

    return result


def _d6label(count: int = 1, critical: bool = False) -> str:
    label = f'{count}D6'
    if critical:
        label += '+'
    return label


class Outcome(Enum):
    """
    Skill checks can result in various outcomes.
    These are explained here.
    """

    CriticalFail = -2
    """
    A critical fail occurs when the roll results in a 1.
    Not only does the check fail immediately, something bad happens as well.
    Hope you didn't just try to defuse a bomb 💥.
    """

    Fail = -1
    """
    If the roll fails to meet the threshold, the task fails, but nothing out of the ordinary happens.
    """

    NearFail = 0
    """
    A near fail occurs when the roll's result is equal to the threshold.
    The task succeeds, but something _inconvenient_ happens in the process.
    For instance, the gun you just used to blast your opponent fails to correctly cycle the next round into the chamber requiring you to fix the jam before being able to fire again.
    """

    Success = 1
    """
    Success occurs when the roll's result exceeds the threshold.
    """

    CriticalSuccess = 2
    """
    A critical success occurs when the roll results in a 20.
    The task succeeds immediately, no matter the threshold.
    If the check is associated with an action that uses a damage roll, the damage roll is critical.
    """


def check(threshold: int, adv: int = 0) -> Outcome:
    """
    A skill check rolls a D20 (optionally with advantage / disadvantage) against a given threshold.
    """

    roll = d20(adv=adv)

    if roll == 1:
        return Outcome.CriticalFail
    elif roll == 20:
        return Outcome.CriticalSuccess
    elif roll < threshold:
        return Outcome.Fail
    elif roll > threshold:
        return Outcome.Success
    else:
        return Outcome.NearFail


def extendedCheck(threshold: int, maxRolls: Optional[int] = None) -> Tuple[Outcome, int]:
    """
    An extended skill check accumulates D20 rolls until, either, a given threshold is reached, or a maximum number of rolls is exhausted.
    Each roll corresponds to a fixed in-game time period spent working on the task.
    If the maximum number of rolls (i.e. time limit) is exhausted, the check fails.
    Rolling a 1 or 20 does not immediately fail or succeed the task.

    Extended checks do not have advantage or disadvantage.
    Advantage and disadvantage can still be reflected by the time spent per roll (e.g. advantage cuts the time per roll in half).

    Example:
    ```
    > extendedCheck(30)
    (<Outcome.Success: 1>, 3)       # Success after 3 rolls

    > extendedCheck(30, 2)
    (<Outcome.Fail: -1>, 2)         # Fail due to exhausting the time limit
    ```
    """

    accumulator = 0
    rollCount = 0
    while accumulator < threshold:
        if maxRolls and rollCount >= maxRolls:
            return Outcome.Fail, maxRolls

        accumulator += d20()
        rollCount += 1

    return Outcome.Success, rollCount


setSeed = random.seed
"""
Allows one to set a specific seed for the random number generator (RNG).
This allows rolls to be reproducible.
"""

verboseRolls = True
"""Enabling this option shows the result of dice rolls."""
