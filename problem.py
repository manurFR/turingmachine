import random
import sys
from copy import copy
from itertools import chain, combinations

from verifiers import VERIFIERS

MAX_TRIES = 10000

DIFF_EASY = 1
DIFF_STANDARD = 2
DIFF_HARD = 3

MAPPING_DIFFICULTY = {"EASY": DIFF_EASY, "STANDARD": DIFF_STANDARD, "HARD": DIFF_HARD}

MAX_VERIFIERS_BY_DIFF = {
    DIFF_EASY: 17,      # one star difficulty (up to verifier 17)
    DIFF_STANDARD: 22,  # two stars difficulty (up to verifier 22)
    DIFF_HARD: 48       # three stars difficulty (all verifiers)
}


class Code(object):
    def __init__(self, blue, yellow, purple):
        self.blue = blue
        self.yellow = yellow
        self.purple = purple

    def __str__(self):
        return f"{self.blue}{self.yellow}{self.purple}"

    def __repr__(self):
        return f"{self.blue}{self.yellow}{self.purple}"


def generate_game(nb_verif=4, diff=DIFF_EASY, include_verifiers=None, include_criterias=None):
    if include_verifiers is None:
        base_verifiers = []
    elif isinstance(include_verifiers, int):
        base_verifiers = [include_verifiers]
    else:
        base_verifiers = include_verifiers

    if include_criterias is None:
        base_criterias = []
    elif isinstance(include_criterias, str):
        base_criterias = [include_criterias]
    else:
        base_criterias = include_criterias

    # loop over include_criterias to add their corresponding verifiers to the base_verifiers if it doesn't include them
    for criteria_name in base_criterias:
        for verif, spec in VERIFIERS.items():
            if criteria_name in spec:
                if verif not in base_verifiers:
                    base_verifiers.append(verif)
                break

    tries = 0
    while True:
        tries += 1
        verifiers = copy(base_verifiers)

        first_pick = True
        while len(verifiers) < nb_verif:
            # on difficulties STANDARD or HARD, at least one verifier must be inside the corresponding category
            if first_pick and diff == DIFF_STANDARD:
                min_range = MAX_VERIFIERS_BY_DIFF[DIFF_EASY] + 1
            elif first_pick and diff == DIFF_HARD:
                min_range = MAX_VERIFIERS_BY_DIFF[DIFF_STANDARD] + 1
            else:
                min_range = 1
            choice = -1
            while choice == -1 or choice in verifiers:
                choice = random.choice(range(min_range, MAX_VERIFIERS_BY_DIFF[diff] + 1))
            verifiers.append(choice)
            first_pick = False
        verifiers.sort()

        criterias_name, criterias_func = [], []
        for idx, verif in enumerate(verifiers):
            available_criterias = list(VERIFIERS[verif].keys())
            for canditate in base_criterias:
                if canditate in available_criterias:
                    choice = canditate
                    break
            else:
                choice = random.choice(available_criterias)

            # I'm almost sure that a few criterias don't actually have a corresponding checkcard! Avoid these.
            while "checkcard" not in VERIFIERS[verif][choice]:
                choice = random.choice(available_criterias)

            criterias_name.append(choice)
            criterias_func.append(VERIFIERS[verif][choice]["crit"])

        code = test_criterias(criterias_func)
        if code:
            break

        if tries >= MAX_TRIES:
            print(f"Sorry, I didn't found a valid game after {MAX_TRIES} tries. Aborting.")
            sys.exit(0)

    return {
        "tries": tries,
        "verifiers": sorted(verifiers),
        "criterias": criterias_name,
        "code": code
    }


def subsets(criterias):
    subs = chain.from_iterable(combinations(criterias, r) for r in range(len(criterias)))
    return [subset for subset in subs if len(subset) >= 2]


def test_criterias(criterias):
    # Does applying all the criterias leave only one possible solution ?..
    solution = one_solution(criterias)
    if solution:
        # ...and does no subset of the criterias already leave one only possible solution ?
        found = False
        for subset in subsets(criterias):
            if one_solution(subset):
                found = True
                break
        if not found:
            return solution
    return None


def one_solution(criterias):
    # new grid with all possible codes
    grid = [Code(blue, yellow, purple) for blue in range(1, 6) for yellow in range(1, 6) for purple in range(1, 6)]
    for crit in criterias:
        grid = crit(grid)
    if len(grid) == 1:
        return grid[0]
    else:
        return None
