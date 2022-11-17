import argparse
import random
import sys
from copy import copy
from itertools import chain, combinations, product

from checkcards import CHECK_CARDS, SYMBOLS
from verifiers import Code, VERIFIERS

MAX_TRIES = 5000

DIFF_EASY = 1
DIFF_STANDARD = 2
DIFF_HARD = 3

MAPPING_DIFFICULTY = {"EASY": DIFF_EASY, "STANDARD": DIFF_STANDARD, "HARD": DIFF_HARD}

MAX_VERIFIERS_BY_DIFF = {
    DIFF_EASY: 17,      # one star difficulty (up to verifier 17)
    DIFF_STANDARD: 22,  # two stars difficulty (up to verifier 22)
    DIFF_HARD: 48       # three stars difficulty (all verifiers)
}


def newgrid():
    return [Code(blue, yellow, purple) for blue in range(1, 6) for yellow in range(1, 6) for purple in range(1, 6)]


def subsets(criterias):
    subs = chain.from_iterable(combinations(criterias, r) for r in range(len(criterias)))
    return [subset for subset in subs if len(subset) >= 2]


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

        while len(verifiers) < nb_verif:
            choice = -1
            while choice == -1 or choice in verifiers:
                choice = random.choice(range(1, MAX_VERIFIERS_BY_DIFF[diff] + 1))
            verifiers.append(choice)
        verifiers.sort()

        criterias_name, criterias_func = [], []
        for idx, verif in enumerate(verifiers):
            available_criterias = list(VERIFIERS[verif].keys())
            choice = None
            for canditate in base_criterias:
                if canditate in available_criterias:
                    choice = canditate
                    break
            else:
                choice = random.choice(available_criterias)

            # temp hack to exclude criterias for which I haven't found the checkcard yet
            while "checkcard" not in VERIFIERS[verif][choice]:
                choice = random.choice(available_criterias)
            # --

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


def display_game(problem):
    print(f"(nb tries: {problem['tries']})")
    symbol = random.choice(SYMBOLS)
    print("Verifiers: " + ' | '.join(f"{verif} [{symbol}: {CHECK_CARDS[VERIFIERS[verif][crit]['checkcard']][symbol]}]"
                                     for verif, crit in zip(problem['verifiers'], problem['criterias'])))


def display_code(problem):
    resp = "N"
    while resp != "y":
        resp = input("Ready to see the solution code ? (y/N) ")
    print("Criterias: " + ' | '.join(crit for crit in problem['criterias']))
    print(f"Code: {problem['code']}")


def codes_for_verifiers(verifiers):
    # loop over all possible criteria permutations
    solutions = {}
    for criterias in product(*[VERIFIERS[v] for v in verifiers]):
        crit_funcs = [VERIFIERS[v][crit_name]["crit"] for v, crit_name in zip(verifiers, criterias)]
        code = test_criterias(crit_funcs)
        if code:
            if str(code) in solutions:
                solutions[str(code)].append(criterias)
            else:
                solutions[str(code)] = [criterias]
    if solutions:
        for code in sorted(solutions.keys()):
            for criterias in solutions[code]:
                print(f"Code: {code} | Criterias: {', '.join(criterias)}")
    else:
        print("Sorry, no solutions found for this set of verifiers.")
    return solutions


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
    grid = newgrid()
    for crit in criterias:
        grid = crit(grid)
    if len(grid) == 1:
        return grid[0]
    else:
        return None


def determine_checkcards(verifiers, symbol, checkcards, solution):
    solutions = codes_for_verifiers(verifiers)
    for nb, criterias in enumerate(solutions[str(solution)]):
        print(f"Solution #{nb + 1} ===")
        for card, crit in zip(checkcards, criterias):
            for idx, mappings in CHECK_CARDS.items():
                if mappings[symbol] == card:
                    card_idx = idx
                    break
            # noinspection PyUnboundLocalVariable
            print(f"Card {card_idx}: {crit} \"checkcard\": {card_idx}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate problems for Turing Machine')
    parser.add_argument('nb_verif', nargs='?', default=4,
                        help='number of verifiers for the problem (4-6)', type=int)
    parser.add_argument('difficulty', nargs='?', default='STANDARD', choices=('EASY', 'STANDARD', 'HARD'),
                        help='difficulty of the problem')
    parser.add_argument('--include-verifiers', nargs='+', metavar='VERIFIER', type=int,
                        help='number(s) of one or more verifiers to force in the problem')
    parser.add_argument('--include-criterias', nargs='+', metavar='CRITERIA', help=argparse.SUPPRESS)
    parser.add_argument('--getcodes', nargs='+', metavar='VERIFIER',
                        help='find all the codes that match the list of one or more verifiers given as parameters '
                             '(aka cheat mode!) - if present, does not generate a problem')

    args = parser.parse_args()

    if args.getcodes:
        codes_for_verifiers(list(int(v) for v in args.getcodes))
    else:
        game = generate_game(args.nb_verif,
                             MAPPING_DIFFICULTY[args.difficulty],
                             include_verifiers=args.include_verifiers,
                             include_criterias=args.include_criterias)
        display_game(game)
        display_code(game)

    # determine_checkcards([19, 25, 27, 34, 39, 44], "pound", [257, 708, 213, 379, 359, 461], 242)
