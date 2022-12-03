SYMBOLS = ["lozenge", "pound", "slash", "currency"]
CHECK_CARDS = {
    1:  {"lozenge": 201, "pound": 798, "slash": 204, "currency": 796},  # purple_eq_4 ?
    2:  {"lozenge": 206, "pound": 793, "slash": 212, "currency": 790},  # no_one
    3:  {"lozenge": 215, "pound": 786, "slash": 217, "currency": 783},  # two_threes
    4:  {"lozenge": 220, "pound": 781, "slash": 223, "currency": 779},  # sum_even ?
    5:  {"lozenge": 227, "pound": 776, "slash": 231, "currency": 773},  # blue_plus_purple_eq_4 ?
    6:  {"lozenge": 233, "pound": 770, "slash": 237, "currency": 767},  # blue_plus_yellow_lt_6
    7:  {"lozenge": 244, "pound": 765, "slash": 251, "currency": 759},  # purple_eq_1 ?
    8:  {"lozenge": 253, "pound": 757, "slash": 256, "currency": 754},  # blue_eq_purple
    9:  {"lozenge": 261, "pound": 750, "slash": 264, "currency": 747},  # one_triple
    10: {"lozenge": 267, "pound": 744, "slash": 270, "currency": 742},  # yellow_plus_purple_eq_6
    11: {"lozenge": 274, "pound": 740, "slash": 278, "currency": 738},  # two_consecutive_asc
    12: {"lozenge": 280, "pound": 736, "slash": 282, "currency": 733},  # descending
    13: {"lozenge": 286, "pound": 729, "slash": 288, "currency": 725},  # sum_is_multiple_of_4
    14: {"lozenge": 293, "pound": 720, "slash": 296, "currency": 718},  # yellow_lt_blue_purple
    15: {"lozenge": 302, "pound": 715, "slash": 304, "currency": 710},  # sum_eq_6 ?
    16: {"lozenge": 309, "pound": 708, "slash": 312, "currency": 704},  # no_consecutive_asc_desc
    17: {"lozenge": 315, "pound": 699, "slash": 317, "currency": 696},  # blue_plus_yellow_gt_6
    18: {"lozenge": 322, "pound": 694, "slash": 325, "currency": 690},  # purple_lt_blue_yellow
    19: {"lozenge": 329, "pound": 687, "slash": 331, "currency": 684},  # yellow_gt_blue_purple
    20: {"lozenge": 334, "pound": 680, "slash": 337, "currency": 673},  # three_consecutive_asc
    21: {"lozenge": 339, "pound": 669, "slash": 341, "currency": 667},  # one_twin
    22: {"lozenge": 346, "pound": 664, "slash": 348, "currency": 662},  # yellow_gt_3
    23: {"lozenge": 350, "pound": 658, "slash": 353, "currency": 656},  # no_consecutive_asc
    24: {"lozenge": 356, "pound": 653, "slash": 358, "currency": 651},  # one_one
    25: {"lozenge": 360, "pound": 649, "slash": 365, "currency": 647},  # three_evens
    26: {"lozenge": 370, "pound": 645, "slash": 373, "currency": 641},  # sum_lt_6
    27: {"lozenge": 376, "pound": 639, "slash": 378, "currency": 637},  # no_fours
    28: {"lozenge": 381, "pound": 635, "slash": 385, "currency": 633},  # one_four
    29: {"lozenge": 387, "pound": 631, "slash": 390, "currency": 629},  # yellow_lt_3
    30: {"lozenge": 392, "pound": 627, "slash": 394, "currency": 621},  # yellow_plus_purple_eq_4
    31: {"lozenge": 396, "pound": 617, "slash": 401, "currency": 615},  # purple_lt_3 ?
    32: {"lozenge": 403, "pound": 613, "slash": 405, "currency": 610},  # purple_even ?
    33: {"lozenge": 407, "pound": 608, "slash": 410, "currency": 605},  # ascending ?
    34: {"lozenge": 413, "pound": 599, "slash": 416, "currency": 597},  # blue_eq_3
    35: {"lozenge": 419, "pound": 595, "slash": 423, "currency": 593},  # yellow_gt_1
    36: {"lozenge": 429, "pound": 591, "slash": 432, "currency": 589},  # purple_gt_1
    37: {"lozenge": 434, "pound": 587, "slash": 437, "currency": 585},  # blue_gt_3
    38: {"lozenge": 440, "pound": 581, "slash": 442, "currency": 579},  # blue_lt_4 ?
    39: {"lozenge": 447, "pound": 577, "slash": 453, "currency": 573},  # yellow_eq_4
    40: {"lozenge": 455, "pound": 571, "slash": 459, "currency": 567},  # two_ones ?
    41: {"lozenge": 462, "pound": 564, "slash": 464, "currency": 562},  # yellow_eq_3 ?
    42: {"lozenge": 470, "pound": 558, "slash": 472, "currency": 553},  # purple_gt_3
    43: {"lozenge": 475, "pound": 550, "slash": 479, "currency": 547},  # purple_le_blue_yellow
    44: {"lozenge": 481, "pound": 543, "slash": 483, "currency": 540},  # yellow_even
    45: {"lozenge": 485, "pound": 536, "slash": 487, "currency": 533},  # no_order
    46: {"lozenge": 491, "pound": 530, "slash": 495, "currency": 527},  # blue_eq_1
    47: {"lozenge": 497, "pound": 523, "slash": 499, "currency": 518},  # no_twin
    48: {"lozenge": 503, "pound": 515, "slash": 505, "currency": 509},  # evens_lt_odds
    49: {"lozenge": 507, "pound": 506, "slash": 514, "currency": 504},  # three_consecutive_asc_desc
    50: {"lozenge": 516, "pound": 502, "slash": 520, "currency": 498},  # no_repeat
    51: {"lozenge": 525, "pound": 496, "slash": 528, "currency": 492},  # no_evens
    52: {"lozenge": 532, "pound": 490, "slash": 534, "currency": 486},  # yellow_odd
    53: {"lozenge": 537, "pound": 484, "slash": 541, "currency": 482},  # one_even
    54: {"lozenge": 546, "pound": 480, "slash": 549, "currency": 476},  # purple_eq_3 ?
    55: {"lozenge": 551, "pound": 474, "slash": 557, "currency": 471},  # sum_is_multiple_of_5
    56: {"lozenge": 560, "pound": 469, "slash": 563, "currency": 463},  # two_fours
    57: {"lozenge": 566, "pound": 461, "slash": 568, "currency": 458},  # blue_lt_yellow / yellow_gt_blue
    58: {"lozenge": 572, "pound": 454, "slash": 576, "currency": 449},  # yellow_le_blue_purple
    59: {"lozenge": 578, "pound": 445, "slash": 580, "currency": 441},  # blue_odd
    60: {"lozenge": 582, "pound": 439, "slash": 586, "currency": 435},  # sum_is_multiple_of_3 ?
    61: {"lozenge": 588, "pound": 433, "slash": 590, "currency": 430},  # yellow_eq_1 ?
    62: {"lozenge": 592, "pound": 424, "slash": 594, "currency": 421},  # sum_odd
    63: {"lozenge": 596, "pound": 418, "slash": 598, "currency": 414},  # blue_lt_yellow_purple
    64: {"lozenge": 604, "pound": 412, "slash": 606, "currency": 409},  # blue_plus_purple_eq_6 ?
    65: {"lozenge": 609, "pound": 406, "slash": 611, "currency": 404},  # purple_gt_blue_yellow
    66: {"lozenge": 614, "pound": 402, "slash": 616, "currency": 399},  # blue_lt_purple
    67: {"lozenge": 618, "pound": 395, "slash": 625, "currency": 393},  # two_evens
    68: {"lozenge": 628, "pound": 391, "slash": 630, "currency": 391},  # blue_eq_4 ?
    69: {"lozenge": 632, "pound": 386, "slash": 634, "currency": 382},  # yellow_gt_purple
    70: {"lozenge": 636, "pound": 379, "slash": 638, "currency": 377},  # blue_le_yellow_purple
    71: {"lozenge": 640, "pound": 374, "slash": 643, "currency": 372},  # evens_gt_odds
    72: {"lozenge": 646, "pound": 369, "slash": 648, "currency": 362},  # no_three
    73: {"lozenge": 650, "pound": 359, "slash": 652, "currency": 357},  # blue_gt_1
    74: {"lozenge": 654, "pound": 355, "slash": 657, "currency": 352},  # purple_odd
    75: {"lozenge": 661, "pound": 349, "slash": 663, "currency": 347},  # blue_gt_yellow_purple
    76: {"lozenge": 665, "pound": 344, "slash": 668, "currency": 340},  # blue_ge_yellow_purple ?
    77: {"lozenge": 670, "pound": 338, "slash": 677, "currency": 335},  # yellow_lt_4
    78: {"lozenge": 681, "pound": 332, "slash": 686, "currency": 330},  # sum_gt_6
    79: {"lozenge": 688, "pound": 327, "slash": 691, "currency": 324},  # yellow_gt_4 ?
    80: {"lozenge": 695, "pound": 319, "slash": 697, "currency": 316},  # blue_gt_purple ?
    81: {"lozenge": 701, "pound": 314, "slash": 706, "currency": 311},  # blue_plus_yellow_eq_4
    82: {"lozenge": 709, "pound": 308, "slash": 714, "currency": 303},  # blue_gt_4 ?
    83: {"lozenge": 717, "pound": 299, "slash": 719, "currency": 294},  # purple_gt_4 ?
    84: {"lozenge": 723, "pound": 289, "slash": 726, "currency": 287},  # blue_gt_yellow
    85: {"lozenge": 737, "pound": 279, "slash": 739, "currency": 277},  # blue_eq_yellow
    86: {"lozenge": 741, "pound": 273, "slash": 743, "currency": 268},  # one_double
    87: {"lozenge": 746, "pound": 266, "slash": 749, "currency": 263},  # two_consecutive_asc_desc
    88: {"lozenge": 751, "pound": 257, "slash": 755, "currency": 255},  # blue_plus_yellow_eq_6
    89: {"lozenge": 758, "pound": 252, "slash": 763, "currency": 247},  # blue_even
    90: {"lozenge": 766, "pound": 243, "slash": 769, "currency": 236},  # yellow_ge_blue_purple ?
    91: {"lozenge": 771, "pound": 232, "slash": 775, "currency": 228},  # yellow_eq_purple
    92: {"lozenge": 778, "pound": 224, "slash": 780, "currency": 221},  # blue_lt_3
    93: {"lozenge": 782, "pound": 219, "slash": 785, "currency": 216},  # one_three
    94: {"lozenge": 787, "pound": 213, "slash": 792, "currency": 207},  # purple_lt_4
    95: {"lozenge": 795, "pound": 205, "slash": 797, "currency": 202}   # yellow_lt_purple
}
