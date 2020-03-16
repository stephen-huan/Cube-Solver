import numpy as np
import random
import cube

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

def gen_moves() -> dict:
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

def move_mat(seq: str) -> np.array:
    """ Turns a sequence of moves into a transformation matrix. """
    T = np.identity(54)
    for move in cube.tokenize(seq):
        T = moves[move] @ T
    return T

def apply(T: np.array, x: cube.Cube) -> cube.Cube:
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

if __name__ == "__main__":
    ### TESTING GENERATION AND EQUAL TO MOVE

    c = distinct_cube()

    x = flatten(c)
    M = perm_mat(x)
    c.turn("R")
    y = flatten(c)
    R = perm_mat(y)

    T = R @ np.linalg.inv(M)

    assert np.array_equal(T @ x, y)

    ### TESTING MAKING A MOVE WITH MATRIX

    c = cube.Cube()
    x = flatten(c)
    c = import_cube(np.linalg.inv(M) @ T @ x)
    # print(c)

    ### FINAL

    # permutation from importing
    M = np.linalg.inv(perm_mat(flatten(distinct_cube())))
    moves = gen_moves()

    c = cube.Cube()
    # print(apply(move_mat("R U"), c))

    # largest group
    T = move_mat("R U2 D' B D'")
    # print(apply(mat_exp(T, 1260), c))

    # what's the state after (R U F L B)100000?
    T = move_mat("R U F L B")
    # print(apply(mat_exp(T, 100000), c))

    # superflip
    TPERM = "R U R' U' R' F R2 U' R' U' R U R' F'"
    SUPERFLIP = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    CHECKER = "F2 B2 U2 D2 R2 L2"

    T = move_mat(TPERM)
    # print(pretty(T))

    ### DIFFICULT SERIES OF MOVES
    # Calculating (((((F' D R' D U2)k (D' R D' F U2)k)k (R' U R' F L2)k)k (R D' F U2 D')k)k (D F' D R' U2)k)k

    k = 10**9 + 7
    orders = ["F' D R' D U2", "D' R D' F U2", "R' U R' F L2", "R D' F U2 D'", "D F' D R' U2"]
    T = mat_exp(move_mat(orders[0]), k)
    for order in orders[1:]:
        T = mat_exp(mat_exp(move_mat(order), k) @ T, k)

    print(apply(T, cube.Cube()))
