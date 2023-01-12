import argparse
import random
import sys

from booklet import generate_games, prepare_booklet
from checkcards import CHECK_CARDS, SYMBOLS
from problem import generate_game, MAPPING_DIFFICULTY, find_all_solutions
from verifiers import VERIFIERS


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


def get_codes(verifiers):
    solutions = find_all_solutions(verifiers)
    if solutions:
        for code in sorted(solutions.keys()):
            for criterias in solutions[code]:
                print(f"Code: {code} | Criterias: {', '.join(criterias)}")
    else:
        print("Sorry, no solutions found for this set of verifiers.")


def determine_checkcards(verifiers, symbol, checkcards, solution):
    solutions = find_all_solutions(verifiers)
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
    parser = argparse.ArgumentParser(description='Unofficial problem generator for Turing Machine',
                                     usage="%(prog)s [-h] { --generate-booklet | --getcodes VERIFIER [VERIFIER ...] | "
                                           "nb_verif [{EASY,STANDARD,HARD} "
                                           "[--include-verifiers VERIFIER [VERIFIER ...]] }",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="Examples:\r\n"
                                            "  python %(prog)s 5 STANDARD\n"
                                            "  python %(prog)s 4 HARD --include-verifiers 12 39\n"
                                            "  python %(prog)s --generate-booket\n"
                                            "  python %(prog)s --getcodes 7 13 24 32")
    parser.add_argument('nb_verif', nargs='?', default=4,
                        help='number of verifiers for the problem (4-6)', type=int)
    parser.add_argument('difficulty', nargs='?', default='STANDARD', choices=('EASY', 'STANDARD', 'HARD'),
                        help='difficulty of the problem')
    parser.add_argument('--include-verifiers', nargs='+', metavar='VERIFIER', type=int,
                        help='number(s) of one or more verifiers to force in the problem')
    parser.add_argument('--include-criterias', nargs='+', metavar='CRITERIA', help=argparse.SUPPRESS)
    parser.add_argument('--generate-booklet', action='store_true',
                        help="create a pdf booklet with many games for each number of verifier and difficulty "
                             "(needs a few minutes to complete)")
    parser.add_argument('--getcodes', nargs='+', metavar='VERIFIER',
                        help='find all the codes that match the list of one or more verifiers given as parameters '
                             '(aka cheat mode!) - if present, does not generate a problem')
    parser.add_argument('--seed', help=argparse.SUPPRESS)

    args = parser.parse_args()

    # take the given seed if provided... or randomly generate it (isn't it ironic, don't you think?)
    random_seed = args.seed if args.seed else random.randrange(99999999)
    random.seed(random_seed)

    if args.generate_booklet:
        if 'fpdf' not in sys.modules:
            print("Aborting.")
            sys.exit(1)
        problems = generate_games()
        prepare_booklet(problems, random_seed)
    elif args.getcodes:
        get_codes(list(int(v) for v in args.getcodes))
    else:
        game = generate_game(args.nb_verif,
                             MAPPING_DIFFICULTY[args.difficulty],
                             include_verifiers=args.include_verifiers,
                             include_criterias=args.include_criterias)
        display_game(game)
        display_code(game)

    # determine_checkcards([19, 25, 27, 34, 39, 44], "pound", [257, 708, 213, 379, 359, 461], 242)
