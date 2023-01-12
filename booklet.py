import os
import random
import timeit
from itertools import product

try:
    from fpdf import FPDF
except ImportError:
    FPDF = object  # hack to allow compilation of class BookletPDF
    print("WARNING: the python fpdf2 library is required to use --generate-booklet. "
          "Do \"python -m pip install fpdf2\".")

from checkcards import SYMBOLS, CHECK_CARDS
from problem import generate_game, MAPPING_DIFFICULTY
from verifiers import VERIFIERS

PROBLEMS_BY_ROW = 5
PROBLEMS_BY_PAGE = PROBLEMS_BY_ROW * 3

TITLE_W = 116
TITLE_H = 10

FRAME_W = 29
FRAME_HEADER = 6
FRAME_VERIFIER_SPACE = 7.7
FRAME_FOOTER = 2
FRAME_PADDING = 3.5

# color names found with https://www.color-blindness.com/color-name-hue/
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SMOKE = (242, 242, 242)
GRAY = (128, 128, 128)
CINNABAR = (230, 67, 34)
MARIGOLD = (183, 127, 57)
EUCALYPTUS = (47, 174, 94)
DELUGE = (125, 116, 151)

SYMBOLS_PROP = {
    "lozenge":  {"color": (45, 167, 90),   "unicode": "\N{LOZENGE}",       "size": 11},
    "pound":    {"color": (239, 155, 26),  "unicode": "#",                 "size": 9},
    "slash":    {"color": (84, 170, 208),  "unicode": "/",                 "size": 8},
    "currency": {"color": (124, 100, 164), "unicode": "\N{CURRENCY SIGN}", "size": 11},
}


def get_frame_height(nb_verif):
    return FRAME_HEADER + (FRAME_VERIFIER_SPACE * nb_verif) + FRAME_FOOTER


def generate_games():
    print("Generating games")
    print("Please wait", end='', flush=True)
    start = timeit.default_timer()
    games = {}
    # for nb_verif, difficulty in product([6], ["EASY"]):
    for nb_verif, difficulty in product([4, 5, 6], MAPPING_DIFFICULTY.keys()):
        games[(nb_verif, difficulty)] = [generate_game(nb_verif, MAPPING_DIFFICULTY[difficulty])
                                         for _ in range(PROBLEMS_BY_PAGE)]
        print('.', end='', flush=True)
    print(flush=True)
    end = timeit.default_timer()
    print(f"Games generated ({(end - start):.2f} seconds elapsed)")
    print()
    return games


class BookletPDF(FPDF):
    def header(self):
        self.set_font("helvetica", size=12)
        self.set_text_color(*BLACK)
        self.cell(0, 20, txt="Turing Machine - Unofficial challenges", align="C", new_x="LMARGIN", new_y="NEXT")

    def print_title(self, title):
        self.set_fill_color(*CINNABAR)
        self.set_text_color(*SMOKE)
        self.rect(x=10, y=15, w=TITLE_W, h=TITLE_H, style='F', round_corners=('TOP_LEFT', 'TOP_RIGHT'))
        self.set_font("helvetica", 'B', size=14)
        self.cell(w=TITLE_W, h=0, txt=title, align='C', new_x="LMARGIN", new_y="NEXT")

    def print_game(self, idx, nb_verif, difficulty, game, x, y):
        symbol = random.choice(SYMBOLS)
        # frame
        self.set_draw_color(*CINNABAR)
        self.set_line_width(0.4)
        self.rect(x, y, w=FRAME_W, h=get_frame_height(nb_verif), style='D', round_corners=True, corner_radius=2)
        # number
        self.set_text_color(*CINNABAR)
        self.set_font("helvetica", 'B', size=15)
        self.text(x+2, y+5, f"{idx+1:02d}")
        # difficulty (gears)
        self.set_text_color(*MARIGOLD)
        self.set_font("everson", 'B', size=16)
        self.set_char_spacing(2)
        self.text(x+10, y+5.5, "\N{Gear Without Hub}"*MAPPING_DIFFICULTY[difficulty])
        self.set_char_spacing(0)
        # verifiers
        vy = y + 12
        for letter, verifier, criteria in zip('ABCDEFG', game['verifiers'], game['criterias']):
            # letter
            self.set_text_color(*EUCALYPTUS)
            self.set_font("helvetica", 'B', size=15)
            self.text(x+3, vy, letter)
            # verifier number
            self.set_fill_color(*EUCALYPTUS)
            self.set_text_color(*SMOKE)
            self.set_font("helvetica", 'B', size=11)
            self.rect(x+10, vy-5.2, 6, 6, style='F', round_corners=True)
            vstr = str(verifier)
            self.text(x+13-(self.get_string_width(vstr)/2), vy-0.6, vstr)
            # check card number and symbol
            self.set_draw_color(*SYMBOLS_PROP[symbol]["color"])
            self.set_line_width(0.35)
            self.rect(x+18, vy-5.2, 9, 6, style='D', round_corners=True)
            self.set_text_color(*SYMBOLS_PROP[symbol]["color"])
            self.text(x+19, vy-0.6, str(CHECK_CARDS[VERIFIERS[verifier][criteria]["checkcard"]][symbol]))
            self.set_fill_color(*WHITE)
            # self.set_line_width(0.1)
            self.rect(x+25.3, vy-6.5, 2.7, 2.7, style='F')  # wipe off top right corner
            self.set_font("everson", 'B', size=SYMBOLS_PROP[symbol]["size"])
            self.text(x+25.5, vy-4, SYMBOLS_PROP[symbol]["unicode"])
            vy += FRAME_VERIFIER_SPACE

    def add_solutions(self, games):
        self.add_page()
        self.print_title("Solutions")
        self.cell(w=0, h=10, new_x="LMARGIN", new_y="NEXT")
        # noinspection PyShadowingNames
        for (nb_verif, difficulty), problems in games.items():
            # section
            self.set_text_color(*CINNABAR)
            self.set_font("helvetica", 'B', size=12)
            section = f"Number of verifiers: {nb_verif} | Difficulty: {difficulty}"
            self.cell(w=TITLE_W, h=3, txt=section, align='L', new_x="LMARGIN", new_y="NEXT")
            self.cell(w=2, h=0, new_x="RIGHT")  # left indent
            # solutions
            for idx, pb in enumerate(problems):
                self.set_text_color(*CINNABAR)
                self.set_font("helvetica", 'B', size=9.5)
                self.cell(w=5.2, h=10, txt=f"{idx+1:02d}:", new_x="RIGHT")
                self.set_text_color(*DELUGE)
                self.set_font("helvetica", size=9.5)
                self.cell(w=7, h=10, txt=f"{pb['code']}", new_x="RIGHT")
            self.cell(w=0, h=14, new_x="LMARGIN", new_y="NEXT")  # line break

    def footer(self):
        self.set_y(-10)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(*BLACK)
        footertext = f"Page {self.page_no()}/{{nb}} - Generated with https://github.com/manurFR/turingmachine"
        # noinspection PyUnresolvedReferences
        if not self.lastpage:
            footertext += f" - solutions on last page"
        self.cell(0, 4, footertext, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "I", 6)
        self.cell(0, 4, "This is fan produced content. It was not made by Scorpion Masqué nor the game authors.",
                  align="C")

    def add_seed(self, seed):
        self.set_font("helvetica", size=7)
        self.set_text_color(*GRAY)
        with self.rotation(90, 105, 105):
            self.text(185, 6, f"seed: {seed}")


def prepare_booklet(games, seed):
    print("Generating booklet")
    # noinspection PyTypeChecker
    pdf = BookletPDF(format=(210, 210))  # 21x21 cm
    pdf.lastpage = False
    pdf.set_display_mode(zoom='fullpage')
    pdf.set_top_margin(0)
    pdf.add_font("everson", "B", "font/EversonMonoBold.ttf")
    # noinspection PyShadowingNames
    for (nb_verif, difficulty), problems in games.items():
        pdf.add_page()
        pdf.print_title(f"Number of verifiers: {nb_verif} | Difficulty: {difficulty}")
        for idx, pb in enumerate(problems):
            x = 20 + (idx % PROBLEMS_BY_ROW) * (FRAME_W + FRAME_PADDING)
            y = 28 + int(idx / PROBLEMS_BY_ROW) * (get_frame_height(nb_verif) + FRAME_PADDING)
            pdf.print_game(idx, nb_verif, difficulty, pb, x, y)
    pdf.add_solutions(games)
    pdf.add_seed(seed)
    outputfile = available_filename()
    pdf.lastpage = True  # this must be declared here because the last footer() call is actually made in output()
    pdf.output(outputfile)
    print(f"Booklet generated as {outputfile}.")


def available_filename():
    base = "TuringMachineBooklet"
    if not os.path.exists(f"{base}.pdf"):
        return f"{base}.pdf"
    idx = 1
    while os.path.exists(f"{base}{idx:03d}.pdf"):
        idx += 1
    return f"{base}{idx:03d}.pdf"


if __name__ == "__main__":
    problems = generate_games()
    prepare_booklet(problems, random.randrange(99999999))
