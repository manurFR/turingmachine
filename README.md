# Turing Machine

This will run on Python 3.x.

This fan-made program is dedicated to the **Turing Machine** boardgame, released by Le Scorpion Masqué in 2022.

It will generate new, unofficial, Problems for the game (either one problem, or a full pdf booklet with more than 100 games). It can also solve existing problems.

Like official problems, every generated games will have only ONE possible solution (ie. one valid code that checks all verifiers).

## Usage : generating a new Problem

    $ python turing.py <nb_verif> <difficulty> [--include-verifiers <verifier1> ...]
    nb_verif : number of verifiers for the problem (4 to 6)
    difficulty : EASY, STANDARD or HARD
    --include-verifiers : optional, add here the number of the verifier(s) you require in your game (space separated)

Note : 
* EASY difficulty include only verifiers 1 to 17; 
* STANDARD only verifiers 1 to 22; 
* HARD include all verifiers from 1 to 48.

### Examples :

    $ python turing.py 4 EASY
Will produce a 4-verifiers problem from the 1-17 range, with only one valid solution.

    $ python turing.py 6 STANDARD --include-verifiers 14
Will produce a 6-verifiers problem from the 1-22 range, that will include verifier number 14 and five others.

    $ python turing.py 5 HARD --include-verifiers 3 40
Will produce a 5-verifiers problems taken from all the available verifiers but including numbers 3, 40 and three others.

### In practice :

    $ python turing.py 5 HARD --include-verifiers 26
    (nb tries: 151)
    Verifiers: 7 [pound: 613] | 26 [pound: 224] | 31 [pound: 595] | 36 [pound: 439] | 42 [pound: 406]
    Ready to see the solution code ? (y/N) y
    Criterias: v07_purple_even | v26_blue_lt_3 | v31_yellow_gt_1 | v36_sum_is_multiple_of_3 | v42_purple_gt_blue_yellow
    Code: 234
    
This asks to set up the game with the five verifiers A: 7 | B: 26 | C: 31 | D: 36 | E: 42 and the verification cards found with the pound ('#') symbol 
under numbers A: 613 | B: 224 | C: 595 | D: 439 | E: 406.

The answer (the code and the relevant criteria that each verifier tests) will only be printed after your confirmation.

## Usage : generating a pdf booklet of problems

**Warning**: This requires the fpdf2 external library. Install it (preferably in a virtualenv) with the command:

    $ python -m pip install fpdf2

Then:

    $ python turing.py --generate-booklet

This will generate a pdf booklet with 9 pages of 15 random games each, for every combination of 4, 5 or 6 verifiers and difficulties EASY, STANDARD or HARD.

_Note:_ It will take 2 to 5 minutes to find 135 valid and interesting problems, depending on your machine. Please be patient.

## Usage : finding all valid solutions for a set of verifiers

    $ python turing.py --getcodes 7 13 24 32
Will list all the codes that work for the given verifiers numbers, and the good criteria (from the list on the card) that each verifier tests.

A set of verifiers can have multiple codes that work as a solution.

It can even have a code that works with different combinations of criterias ; it will be printed as many times as these.

### Example

    $ python turing.py --getcodes 7 13 24 32
    Code: 344 | Criterias: v07_purple_even, v13_yellow_eq_purple, v24_two_consecutive_asc, v32_yellow_gt_3
    Code: 344 | Criterias: v07_purple_even, v13_yellow_eq_purple, v24_two_consecutive_asc, v32_purple_gt_3
    Code: 455 | Criterias: v07_purple_odd, v13_yellow_eq_purple, v24_two_consecutive_asc, v32_yellow_gt_3
    Code: 455 | Criterias: v07_purple_odd, v13_yellow_eq_purple, v24_two_consecutive_asc, v32_purple_gt_3

In this example, the set of verifiers 7, 13, 24 and 32 has two possible solutions but each with two combinations of criterias possible. 
For instance, the code 344 is the solution whether the verifier 32 is testing that Yellow > 3 or that Purple > 3.
