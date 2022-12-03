from re import match

VERIFIERS = {
    1: {
        "v01_blue_eq_1": {"crit": lambda grid: [code for code in grid if code.blue == 1], "checkcard": 46},
        "v01_blue_gt_1": {"crit": lambda grid: [code for code in grid if code.blue > 1], "checkcard": 73}
    },
    2: {
        "v02_blue_lt_3": {"crit": lambda grid: [code for code in grid if code.blue < 3], "checkcard": 92},
        "v02_blue_eq_3": {"crit": lambda grid: [code for code in grid if code.blue == 3], "checkcard": 34},
        "v02_blue_gt_3": {"crit": lambda grid: [code for code in grid if code.blue > 3], "checkcard": 37}
    },
    3: {
        "v03_yellow_lt_3": {"crit": lambda grid: [code for code in grid if code.yellow < 3], "checkcard": 29},
        "v03_yellow_eq_3": {"crit": lambda grid: [code for code in grid if code.yellow == 3], "checkcard": 41},
        "v03_yellow_gt_3": {"crit": lambda grid: [code for code in grid if code.yellow > 3], "checkcard": 22}
    },
    4: {
        "v04_yellow_lt_4": {"crit": lambda grid: [code for code in grid if code.yellow < 4], "checkcard": 77},
        "v04_yellow_eq_4": {"crit": lambda grid: [code for code in grid if code.yellow == 4], "checkcard": 39},
        "v04_yellow_gt_4": {"crit": lambda grid: [code for code in grid if code.yellow > 4], "checkcard": 79}
    },
    5: {
        "v05_blue_even": {"crit": lambda grid: [code for code in grid if code.blue % 2 == 0], "checkcard": 89},
        "v05_blue_odd":  {"crit": lambda grid: [code for code in grid if code.blue % 2 == 1], "checkcard": 59}
    },
    6: {
        "v06_yellow_even": {"crit": lambda grid: [code for code in grid if code.yellow % 2 == 0], "checkcard": 44},
        "v06_yellow_odd":  {"crit": lambda grid: [code for code in grid if code.yellow % 2 == 1], "checkcard": 52}
    },
    7: {
        "v07_purple_even": {"crit": lambda grid: [code for code in grid if code.purple % 2 == 0], "checkcard": 32},
        "v07_purple_odd":  {"crit": lambda grid: [code for code in grid if code.purple % 2 == 1], "checkcard": 74}
    },
    8: {
        "v08_no_one":     {"crit": lambda grid: [code for code in grid if str(code).count('1') == 0], "checkcard": 2},
        "v08_one_one":    {"crit": lambda grid: [code for code in grid if str(code).count('1') == 1], "checkcard": 24},
        "v08_two_ones":   {"crit": lambda grid: [code for code in grid if str(code).count('1') == 2], "checkcard": 40},
        "v08_three_ones": {"crit": lambda grid: [code for code in grid if str(code).count('1') == 3]}
    },
    9: {
        "v09_no_three":     {"crit": lambda grid: [code for code in grid if str(code).count('3') == 0],
                             "checkcard": 72},
        "v09_one_three":    {"crit": lambda grid: [code for code in grid if str(code).count('3') == 1],
                             "checkcard": 93},
        "v09_two_threes":   {"crit": lambda grid: [code for code in grid if str(code).count('3') == 2],
                             "checkcard": 3},
        "v09_three_threes": {"crit": lambda grid: [code for code in grid if str(code).count('3') == 3]}
    },
    10: {
        "v10_no_fours":    {"crit": lambda grid: [code for code in grid if str(code).count('4') == 0], "checkcard": 27},
        "v10_one_four":    {"crit": lambda grid: [code for code in grid if str(code).count('4') == 1], "checkcard": 28},
        "v10_two_fours":   {"crit": lambda grid: [code for code in grid if str(code).count('4') == 2], "checkcard": 56},
        "v10_three_fours": {"crit": lambda grid: [code for code in grid if str(code).count('4') == 3]}
    },
    11: {
        "v11_blue_lt_yellow": {"crit": lambda grid: [code for code in grid if code.blue < code.yellow],
                               "checkcard": 57},
        "v11_blue_eq_yellow": {"crit": lambda grid: [code for code in grid if code.blue == code.yellow],
                               "checkcard": 85},
        "v11_blue_gt_yellow": {"crit": lambda grid: [code for code in grid if code.blue > code.yellow],
                               "checkcard": 84}
    },
    12: {
        "v12_blue_lt_purple": {"crit": lambda grid: [code for code in grid if code.blue < code.purple],
                               "checkcard": 66},
        "v12_blue_eq_purple": {"crit": lambda grid: [code for code in grid if code.blue == code.purple],
                               "checkcard": 8},
        "v12_blue_gt_purple": {"crit": lambda grid: [code for code in grid if code.blue > code.purple],
                               "checkcard": 80},
    },
    13: {
        "v13_yellow_lt_purple": {"crit": lambda grid: [code for code in grid if code.yellow < code.purple],
                                 "checkcard": 95},
        "v13_yellow_eq_purple": {"crit": lambda grid: [code for code in grid if code.yellow == code.purple],
                                 "checkcard": 91},
        "v13_yellow_gt_purple": {"crit": lambda grid: [code for code in grid if code.yellow > code.purple],
                                 "checkcard": 69},
    },
    14: {
        "v14_blue_lt_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue < code.yellow and code.blue < code.purple],
                                      "checkcard": 63},
        "v14_yellow_lt_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow < code.blue and code.yellow < code.purple],
                                      "checkcard": 14},
        "v14_purple_lt_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple < code.blue and code.purple < code.yellow],
                                      "checkcard": 18},
    },
    15: {
        "v15_blue_gt_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue > code.yellow and code.blue > code.purple],
                                      "checkcard": 75},
        "v15_yellow_gt_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow > code.blue and code.yellow > code.purple],
                                      "checkcard": 19},
        "v15_purple_gt_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple > code.blue and code.purple > code.yellow],
                                      "checkcard": 65},
    },
    16: {
        "v16_evens_gt_odds": {"crit": lambda grid: [code for code in grid if evens(code) > odds(code)],
                              "checkcard": 71},
        "v16_evens_lt_odds": {"crit": lambda grid: [code for code in grid if evens(code) < odds(code)],
                              "checkcard": 48},
    },
    17: {
        "v17_no_evens":    {"crit": lambda grid: [code for code in grid if evens(code) == 0], "checkcard": 51},
        "v17_one_even":    {"crit": lambda grid: [code for code in grid if evens(code) == 1], "checkcard": 53},
        "v17_two_evens":   {"crit": lambda grid: [code for code in grid if evens(code) == 2], "checkcard": 67},
        "v17_three_evens": {"crit": lambda grid: [code for code in grid if evens(code) == 3], "checkcard": 25},
    },
    18: {
        "v18_sum_even": {"crit": lambda grid: [code for code in grid
                                               if (code.blue + code.yellow + code.purple) % 2 == 0],
                         "checkcard": 4},
        "v18_sum_odd":  {"crit": lambda grid: [code for code in grid
                                               if (code.blue + code.yellow + code.purple) % 2 == 1],
                         "checkcard": 62},
    },
    19: {
        "v19_blue_plus_yellow_lt_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow) < 6],
                                      "checkcard": 6},
        "v19_blue_plus_yellow_eq_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow) == 6],
                                      "checkcard": 88},
        "v19_blue_plus_yellow_gt_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow) > 6],
                                      "checkcard": 17},
    },
    20: {
        "v20_no_repeat":  {"crit": lambda grid: [code for code in grid if len(set(str(code))) == 3],
                           "checkcard": 50},
        "v20_one_double": {"crit": lambda grid: [code for code in grid if len(set(str(code))) == 2],
                           "checkcard": 86},
        "v20_one_triple": {"crit": lambda grid: [code for code in grid if len(set(str(code))) == 1],
                           "checkcard": 9},
    },
    21: {
        "v21_no_twin":  {"crit": lambda grid: [code for code in grid if len(set(str(code))) != 2], "checkcard": 47},
        "v21_one_twin": {"crit": lambda grid: [code for code in grid if len(set(str(code))) == 2], "checkcard": 21},
    },
    22: {
        "v22_ascending":  {"crit": lambda grid: [code for code in grid if code.blue < code.yellow < code.purple],
                           "checkcard": 33},
        "v22_descending": {"crit": lambda grid: [code for code in grid if code.blue > code.yellow > code.purple],
                           "checkcard": 12},
        "v22_no_order":   {"crit": lambda grid: [code for code in grid
                                                 if not code.blue < code.yellow < code.purple
                                                 and not code.blue > code.yellow > code.purple],
                           "checkcard": 45},
    },
    23: {
        "v23_sum_lt_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow + code.purple) < 6],
                         "checkcard": 26},
        "v23_sum_eq_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow + code.purple) == 6],
                         "checkcard": 15},
        "v23_sum_gt_6": {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow + code.purple) > 6],
                         "checkcard": 78},
    },
    24: {
        "v24_no_consecutive_asc":    {"crit": lambda grid: [code for code in grid
                                                            if match(r"([^5][^5])", consec(code))],
                                      "checkcard": 23},
        "v24_two_consecutive_asc":   {"crit": lambda grid: [code for code in grid
                                                            if match(r"(5[^5]|[^5]5)", consec(code))],
                                      "checkcard": 11},
        "v24_three_consecutive_asc": {"crit": lambda grid: [code for code in grid if consec(code) == '55'],
                                      "checkcard": 20},
    },
    25: {
        "v25_no_consecutive_asc_desc":    {"crit": lambda grid: [code for code in grid
                                                                 if match(r"([^35][^35])", consec(code))],
                                           "checkcard": 16},
        "v25_two_consecutive_asc_desc":   {"crit": lambda grid: [code for code in grid
                                                                 if match(r"(3[^3]|[^3]3|5[^5]|[^5]5)", consec(code))],
                                           "checkcard": 87},
        "v25_three_consecutive_asc_desc": {"crit": lambda grid: [code for code in grid
                                                                 if consec(code) in ('33', '55')],
                                           "checkcard": 49},
    },
    26: {
        "v26_blue_lt_3":   {"crit": lambda grid: [code for code in grid if code.blue < 3], "checkcard": 92},
        "v26_yellow_lt_3": {"crit": lambda grid: [code for code in grid if code.yellow < 3], "checkcard": 29},
        "v26_purple_lt_3": {"crit": lambda grid: [code for code in grid if code.purple < 3], "checkcard": 31},
    },
    27: {
        "v27_blue_lt_4":   {"crit": lambda grid: [code for code in grid if code.blue < 4], "checkcard": 38},
        "v27_yellow_lt_4": {"crit": lambda grid: [code for code in grid if code.yellow < 4], "checkcard": 77},
        "v27_purple_lt_4": {"crit": lambda grid: [code for code in grid if code.purple < 4], "checkcard": 94},
    },
    28: {
        "v28_blue_eq_1":   {"crit": lambda grid: [code for code in grid if code.blue == 1], "checkcard": 46},
        "v28_yellow_eq_1": {"crit": lambda grid: [code for code in grid if code.yellow == 1], "checkcard": 61},
        "v28_purple_eq_1": {"crit": lambda grid: [code for code in grid if code.purple == 1], "checkcard": 7},
    },
    29: {
        "v29_blue_eq_3":   {"crit": lambda grid: [code for code in grid if code.blue == 3], "checkcard": 34},
        "v29_yellow_eq_3": {"crit": lambda grid: [code for code in grid if code.yellow == 3], "checkcard": 41},
        "v29_purple_eq_3": {"crit": lambda grid: [code for code in grid if code.purple == 3], "checkcard": 54},
    },
    30: {
        "v30_blue_eq_4":   {"crit": lambda grid: [code for code in grid if code.blue == 4], "checkcard": 68},
        "v30_yellow_eq_4": {"crit": lambda grid: [code for code in grid if code.yellow == 4], "checkcard": 39},
        "v30_purple_eq_4": {"crit": lambda grid: [code for code in grid if code.purple == 4], "checkcard": 1},
    },
    31: {
        "v31_blue_gt_1":   {"crit": lambda grid: [code for code in grid if code.blue > 1], "checkcard": 73},
        "v31_yellow_gt_1": {"crit": lambda grid: [code for code in grid if code.yellow > 1], "checkcard": 35},
        "v31_purple_gt_1": {"crit": lambda grid: [code for code in grid if code.purple > 1], "checkcard": 36},
    },
    32: {
        "v32_blue_gt_3":   {"crit": lambda grid: [code for code in grid if code.blue > 3], "checkcard": 37},
        "v32_yellow_gt_3": {"crit": lambda grid: [code for code in grid if code.yellow > 3], "checkcard": 22},
        "v32_purple_gt_3": {"crit": lambda grid: [code for code in grid if code.purple > 3], "checkcard": 42},
    },
    33: {
        "v33_blue_even":   {"crit": lambda grid: [code for code in grid if code.blue % 2 == 0], "checkcard": 89},
        "v33_blue_odd":    {"crit": lambda grid: [code for code in grid if code.blue % 2 == 1], "checkcard": 59},
        "v33_yellow_even": {"crit": lambda grid: [code for code in grid if code.yellow % 2 == 0], "checkcard": 44},
        "v33_yellow_odd":  {"crit": lambda grid: [code for code in grid if code.yellow % 2 == 1], "checkcard": 52},
        "v33_purple_even": {"crit": lambda grid: [code for code in grid if code.purple % 2 == 0], "checkcard": 32},
        "v33_purple_odd":  {"crit": lambda grid: [code for code in grid if code.purple % 2 == 1], "checkcard": 74},
    },
    34: {
        "v34_blue_le_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue <= code.yellow and code.blue <= code.purple],
                                      "checkcard": 70},
        "v34_yellow_le_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow <= code.blue and code.yellow <= code.purple],
                                      "checkcard": 58},
        "v34_purple_le_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple <= code.blue and code.purple <= code.yellow],
                                      "checkcard": 43},
    },
    35: {
        "v35_blue_ge_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue >= code.yellow and code.blue >= code.purple],
                                      "checkcard": 76},
        "v35_yellow_ge_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow >= code.blue and code.yellow >= code.purple],
                                      "checkcard": 90},
        "v35_purple_ge_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple >= code.blue and code.purple >= code.yellow]}
    },
    36: {
        "v36_sum_is_multiple_of_3": {"crit": lambda grid: [code for code in grid
                                                           if (code.blue + code.yellow + code.purple) % 3 == 0],
                                     "checkcard": 60},
        "v36_sum_is_multiple_of_4": {"crit": lambda grid: [code for code in grid
                                                           if (code.blue + code.yellow + code.purple) % 4 == 0],
                                     "checkcard": 13},
        "v36_sum_is_multiple_of_5": {"crit": lambda grid: [code for code in grid
                                                           if (code.blue + code.yellow + code.purple) % 5 == 0],
                                     "checkcard": 55},
    },
    37: {
        "v37_blue_plus_yellow_eq_4":   {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow) == 4],
                                        "checkcard": 81},
        "v37_yellow_plus_purple_eq_4": {"crit": lambda grid: [code for code in grid
                                                              if (code.yellow + code.purple) == 4],
                                        "checkcard": 30},
        "v37_blue_plus_purple_eq_4":   {"crit": lambda grid: [code for code in grid if (code.blue + code.purple) == 4],
                                        "checkcard": 5},
    },
    38: {
        "v38_blue_plus_yellow_eq_6":   {"crit": lambda grid: [code for code in grid if (code.blue + code.yellow) == 6],
                                        "checkcard": 88},
        "v38_yellow_plus_purple_eq_6": {"crit": lambda grid: [code for code in grid
                                                              if (code.yellow + code.purple) == 6],
                                        "checkcard": 10},
        "v38_blue_plus_purple_eq_6":   {"crit": lambda grid: [code for code in grid if (code.blue + code.purple) == 6],
                                        "checkcard": 64},
    },
    39: {
        "v39_blue_eq_1":   {"crit": lambda grid: [code for code in grid if code.blue == 1], "checkcard": 46},
        "v39_blue_gt_1":   {"crit": lambda grid: [code for code in grid if code.blue > 1], "checkcard": 73},
        "v39_yellow_eq_1": {"crit": lambda grid: [code for code in grid if code.yellow == 1], "checkcard": 61},
        "v39_yellow_gt_1": {"crit": lambda grid: [code for code in grid if code.yellow > 1], "checkcard": 35},
        "v39_purple_eq_1": {"crit": lambda grid: [code for code in grid if code.purple == 1], "checkcard": 7},
        "v39_purple_gt_1": {"crit": lambda grid: [code for code in grid if code.purple > 1], "checkcard": 36},
    },
    40: {
        "v40_blue_lt_3":   {"crit": lambda grid: [code for code in grid if code.blue < 3], "checkcard": 92},
        "v40_blue_eq_3":   {"crit": lambda grid: [code for code in grid if code.blue == 3], "checkcard": 34},
        "v40_blue_gt_3":   {"crit": lambda grid: [code for code in grid if code.blue > 3], "checkcard": 37},
        "v40_yellow_lt_3": {"crit": lambda grid: [code for code in grid if code.yellow < 3], "checkcard": 29},
        "v40_yellow_eq_3": {"crit": lambda grid: [code for code in grid if code.yellow == 3], "checkcard": 41},
        "v40_yellow_gt_3": {"crit": lambda grid: [code for code in grid if code.yellow > 3], "checkcard": 22},
        "v40_purple_lt_3": {"crit": lambda grid: [code for code in grid if code.purple < 3], "checkcard": 31},
        "v40_purple_eq_3": {"crit": lambda grid: [code for code in grid if code.purple == 3], "checkcard": 54},
        "v40_purple_gt_3": {"crit": lambda grid: [code for code in grid if code.purple > 3], "checkcard": 42},
    },
    41: {
        "v41_blue_lt_4":   {"crit": lambda grid: [code for code in grid if code.blue < 4], "checkcard": 38},
        "v41_blue_eq_4":   {"crit": lambda grid: [code for code in grid if code.blue == 4], "checkcard": 68},
        "v41_blue_gt_4":   {"crit": lambda grid: [code for code in grid if code.blue > 4], "checkcard": 82},
        "v41_yellow_lt_4": {"crit": lambda grid: [code for code in grid if code.yellow < 4], "checkcard": 77},
        "v41_yellow_eq_4": {"crit": lambda grid: [code for code in grid if code.yellow == 4], "checkcard": 39},
        "v41_yellow_gt_4": {"crit": lambda grid: [code for code in grid if code.yellow > 4], "checkcard": 79},
        "v41_purple_lt_4": {"crit": lambda grid: [code for code in grid if code.purple < 4], "checkcard": 94},
        "v41_purple_eq_4": {"crit": lambda grid: [code for code in grid if code.purple == 4], "checkcard": 1},
        "v41_purple_gt_4": {"crit": lambda grid: [code for code in grid if code.purple > 4], "checkcard": 83},
    },
    42: {
        "v42_blue_lt_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue < code.yellow and code.blue < code.purple],
                                      "checkcard": 63},
        "v42_yellow_lt_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow < code.blue and code.yellow < code.purple],
                                      "checkcard": 14},
        "v42_purple_lt_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple < code.blue and code.purple < code.yellow],
                                      "checkcard": 18},
        "v42_blue_gt_yellow_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.blue > code.yellow and code.blue > code.purple],
                                      "checkcard": 75},
        "v42_yellow_gt_blue_purple": {"crit": lambda grid: [code for code in grid
                                                            if code.yellow > code.blue and code.yellow > code.purple],
                                      "checkcard": 19},
        "v42_purple_gt_blue_yellow": {"crit": lambda grid: [code for code in grid
                                                            if code.purple > code.blue and code.purple > code.yellow],
                                      "checkcard": 65},
    },
    43: {
        "v43_blue_lt_yellow": {"crit": lambda grid: [code for code in grid if code.blue < code.yellow],
                               "checkcard": 57},
        "v43_blue_eq_yellow": {"crit": lambda grid: [code for code in grid if code.blue == code.yellow],
                               "checkcard": 85},
        "v43_blue_gt_yellow": {"crit": lambda grid: [code for code in grid if code.blue > code.yellow],
                               "checkcard": 84},
        "v43_blue_lt_purple": {"crit": lambda grid: [code for code in grid if code.blue < code.purple],
                               "checkcard": 66},
        "v43_blue_eq_purple": {"crit": lambda grid: [code for code in grid if code.blue == code.purple],
                               "checkcard": 8},
        "v43_blue_gt_purple": {"crit": lambda grid: [code for code in grid if code.blue > code.purple],
                               "checkcard": 80},
    },
    44: {
        "v44_blue_gt_yellow":   {"crit": lambda grid: [code for code in grid if code.yellow < code.blue],
                                 "checkcard": 84},
        "v44_blue_eq_yellow":   {"crit": lambda grid: [code for code in grid if code.yellow == code.blue],
                                 "checkcard": 85},
        "v44_blue_lt_yellow":   {"crit": lambda grid: [code for code in grid if code.yellow > code.blue],
                                 "checkcard": 57},
        "v44_yellow_lt_purple": {"crit": lambda grid: [code for code in grid if code.yellow < code.purple],
                                 "checkcard": 95},
        "v44_yellow_eq_purple": {"crit": lambda grid: [code for code in grid if code.yellow == code.purple],
                                 "checkcard": 91},
        "v44_yellow_gt_purple": {"crit": lambda grid: [code for code in grid if code.yellow > code.purple],
                                 "checkcard": 69},
    },
    45: {
        "v45_no_one":       {"crit": lambda grid: [code for code in grid if str(code).count('1') == 0],
                             "checkcard": 2},
        "v45_one_one":      {"crit": lambda grid: [code for code in grid if str(code).count('1') == 1],
                             "checkcard": 24},
        "v45_two_ones":     {"crit": lambda grid: [code for code in grid if str(code).count('1') == 2],
                             "checkcard": 40},
        "v45_three_ones":   {"crit": lambda grid: [code for code in grid if str(code).count('1') == 3]},
        "v45_no_three":     {"crit": lambda grid: [code for code in grid if str(code).count('3') == 0],
                             "checkcard": 72},
        "v45_one_three":    {"crit": lambda grid: [code for code in grid if str(code).count('3') == 1],
                             "checkcard": 93},
        "v45_two_threes":   {"crit": lambda grid: [code for code in grid if str(code).count('3') == 2],
                             "checkcard": 3},
        "v45_three_threes": {"crit": lambda grid: [code for code in grid if str(code).count('3') == 3]},
    },
    46: {
        "v46_no_three":     {"crit": lambda grid: [code for code in grid if str(code).count('3') == 0],
                             "checkcard": 72},
        "v46_one_three":    {"crit": lambda grid: [code for code in grid if str(code).count('3') == 1],
                             "checkcard": 93},
        "v46_two_threes":   {"crit": lambda grid: [code for code in grid if str(code).count('3') == 2],
                             "checkcard": 3},
        "v46_three_threes": {"crit": lambda grid: [code for code in grid if str(code).count('3') == 3]},
        "v46_no_fours":     {"crit": lambda grid: [code for code in grid if str(code).count('4') == 0],
                             "checkcard": 27},
        "v46_one_four":     {"crit": lambda grid: [code for code in grid if str(code).count('4') == 1],
                             "checkcard": 28},
        "v46_two_fours":    {"crit": lambda grid: [code for code in grid if str(code).count('4') == 2],
                             "checkcard": 56},
        "v46_three_fours":  {"crit": lambda grid: [code for code in grid if str(code).count('4') == 3]},
    },
    47: {
        "v47_no_one":      {"crit": lambda grid: [code for code in grid if str(code).count('1') == 0], "checkcard": 2},
        "v47_one_one":     {"crit": lambda grid: [code for code in grid if str(code).count('1') == 1], "checkcard": 24},
        "v47_two_ones":    {"crit": lambda grid: [code for code in grid if str(code).count('1') == 2], "checkcard": 40},
        "v47_three_ones":  {"crit": lambda grid: [code for code in grid if str(code).count('1') == 3]},
        "v47_no_fours":    {"crit": lambda grid: [code for code in grid if str(code).count('4') == 0], "checkcard": 27},
        "v47_one_four":    {"crit": lambda grid: [code for code in grid if str(code).count('4') == 1], "checkcard": 28},
        "v47_two_fours":   {"crit": lambda grid: [code for code in grid if str(code).count('4') == 2], "checkcard": 56},
        "v47_three_fours": {"crit": lambda grid: [code for code in grid if str(code).count('4') == 3]},
    },
    48: {
        "v48_blue_lt_yellow":   {"crit": lambda grid: [code for code in grid if code.blue < code.yellow],
                                 "checkcard": 57},
        "v48_blue_eq_yellow":   {"crit": lambda grid: [code for code in grid if code.blue == code.yellow],
                                 "checkcard": 85},
        "v48_blue_gt_yellow":   {"crit": lambda grid: [code for code in grid if code.blue > code.yellow],
                                 "checkcard": 84},
        "v48_blue_lt_purple":   {"crit": lambda grid: [code for code in grid if code.blue < code.purple],
                                 "checkcard": 66},
        "v48_blue_eq_purple":   {"crit": lambda grid: [code for code in grid if code.blue == code.purple],
                                 "checkcard": 8},
        "v48_blue_gt_purple":   {"crit": lambda grid: [code for code in grid if code.blue > code.purple],
                                 "checkcard": 80},
        "v48_yellow_lt_purple": {"crit": lambda grid: [code for code in grid if code.yellow < code.purple],
                                 "checkcard": 95},
        "v48_yellow_eq_purple": {"crit": lambda grid: [code for code in grid if code.yellow == code.purple],
                                 "checkcard": 91},
        "v48_yellow_gt_purple": {"crit": lambda grid: [code for code in grid if code.yellow > code.purple],
                                 "checkcard": 69},
    }
}


def evens(code): return str(code).count('2') + str(code).count('4')
def odds(code): return str(code).count('1') + str(code).count('3') + str(code).count('5')
def consec(code): return f"{4 + code.yellow - code.blue}{4 + code.purple - code.yellow}"

# === CRITERIAS without a corresponding CHECKCARD OMG! ===

# three_ones
# three_threes
# three_fours
# purple_ge_blue_yellow
