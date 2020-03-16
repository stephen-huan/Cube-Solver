import numpy as np
import random
import cube.cube as cube

# https://en.wikipedia.org/wiki/Permutation_matrix
# It's astounding what linear can teach you!

def import_cube(data: list) -> cube.Cube:
    """ Returns a cube, given a length 54 list. """
    c = [cube.list_mat(data[:9])] + [[data[i:i + 3] for i in range(j, 43, 12)] for j in range(9, 21, 3)] + [cube.list_mat(data[-9:])]

    obj = cube.Cube()
    obj.cube = cube.str_cubies(c)
    return obj

def distinct_cube() -> cube.Cube:
    """ Returns a cube with distinct ids for each sticker. """
    return import_cube(list(range(54)))

def perm_mat(perm: list) -> np.array:
    """ Generates a permutation matrix, assuming the standard is 0, 1, ... n."""
    n = len(perm)
    M, I = np.identity(n), np.identity(n)
    for i in range(n):
        M[i] = I[perm[i]]
    return M

def flatten(c: cube.Cube) -> np.array:
    """ Flatten a cube into a 54x1 vector. """
    return np.array([x for row in np.array(c.to_face()) for x in row])

def pretty(T: np.array) -> str:
    """ Pretty-formats a transformation matrix. """
    return "\n".join("".join(str(int(x)) for x in row).replace("0", " ") for row in T)

def latex(T: np.array) -> str:
    """ LaTeX formats a transformation matrix. """
    s = "\\begin{bmatrix}\n"
    s += "\\\ \n".join(" & ".join(str(int(x)) for x in row).replace("0", "0") for row in T)
    s += "\n\\end{bmatrix}"
    return s

def gen_moves(M: np.array) -> dict:
    """ Generates a move dictionary for the 18 standard moves. """
    d = {}
    c = distinct_cube()
    for move in cube.MOVES:
        c.turn(move)
        P = perm_mat(flatten(c))
        d[move] = P @ M
        d[move + "'"] = d[move].T
        d[move + "2"] = d[move] @ d[move]
        c.turn(move + "'")
    return d

def move_mat(seq: str, moves: dict) -> np.array:
    """ Turns a sequence of moves into a transformation matrix. """
    T = np.identity(54)
    for move in cube.tokenize(seq):
        T = moves[move] @ T
    return T

def apply(T: np.array, M: np.array, x: cube.Cube) -> cube.Cube:
    """ Applies the given transformation matrix to the cube. """
    return import_cube(M @ T @ flatten(x))

def mat_exp(A: np.array, k: int) -> list:
    """ Does fast matrix exponentation """
    v = np.identity(len(A))
    while k > 0:
        if k & 1 == 1:
            v = v @ A
        k >>= 1
        A = A @ A
    return v

