import platform

""" Library for coloring purposes. """

windows = platform.system() == "Windows"

ESC = "^<ESC^>" if windows else "\033"
TILE = "█"
MODE = None if windows else 2

def print_color(s, control): return f"{ESC}[{control}m{s}{ESC}[0m"

def color(s, mode=MODE):
    colors8 = {"W": "37",
               "Y": "33",
               "G": "32",
               "B": "34",
               "O": "35",
               "R": "31"
              }
    colors16 = {k: str(int(v) + 60) for k, v in colors8.items()}
    colors256 = {"W": "38;5;245",
                 "Y": "38;5;11",
                 "G": "38;5;10",
                 "B": "38;5;12",
                 "O": "38;5;208",
                 "R": "38;5;9"
                }

    colors = {None: {}, 0: colors8, 1:colors16, 2:colors256}[mode]
    return "".join((print_color(TILE, colors[ch]) if ch in colors else ch for ch in s))

def test_colors():
    """ Prints a nicely formatted table of color sequences; only works on certain terminals. """
    for i in range(256):
        if i % 16 == 0 and i != 0: print()
        print(print_color(str(i) + " "*(4 - len(str(i))), f"48;5;{i}"), end="")
    print()

def contrast(colors): return "".join((print_color(TILE*4, color) for color in colors))

def try_colors():
    f = lambda l: contrast(["38;5;" + str(s) for s in l])

    print(f([*range(160, 162), *range(166, 169), *range(172, 176), 202, 203, 208, 209, *range(214, 219)]))
    print(print_color(TILE*32, "38;5;208"))

if __name__ == "__main__":
    test_colors()
