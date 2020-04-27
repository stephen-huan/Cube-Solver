import random
import cube.cube as cube
import numpy as np
from linear.linear import *

def diag(m):
    values, vectors = np.linalg.eig(move_mat(m, moves))
    d = np.diag(np.round(values, 3))
    return vectors, d

def mult(l1: list, l2: list) -> list:
    """ Applies permutation l2 to l1. """
    return [l1[n] for n in l2]

if __name__ == "__main__":
    # U move written as other moves
    # c = cube.Cube()
    # c.turn("U")
    # noU = cube.Metric(cube.mat_list(((move, move + "'", move + "2") for move in "DFBRL")))
    # print(cube.IDsolve(c, metric=noU)[:-1])
    # exit()

    print(mult(["a", "b", "c", "d", "e"], [2, 4, 0, 1, 3]))

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
    moves = gen_moves(M)

    c = cube.Cube()
    # print(apply(move_mat("R U"), M, c))

    # largest group
    T = move_mat("R U2 D' B D'", moves)
    # print(apply(mat_exp(T, 1260), M, c))

    # what's the state after (R U F L B)100000?
    T = move_mat("R U F L B", moves)
    # print(apply(mat_exp(T, 100000), M, c))

    # superflip
    TPERM = "R U R' U' R' F R2 U' R' U' R U R' F'"
    SUPERFLIP = "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    CHECKER = "F2 B2 U2 D2 R2 L2"
    UPERM = "R2 U R U R' U' R' U' R' U R'"

    T = move_mat(TPERM, moves)
    # print(pretty(T))

    U = move_mat(UPERM, moves)
    # print(pretty(U))
    # u = np.linalg.eig(U)[1][0]
    # print(np.array_equal(U @ u, u))
    # print(set(np.linalg.eigvals(U)))
    # print(set(np.linalg.eigvals(move_mat("U", moves))))
    p, d = diag(TPERM)
    pi = np.linalg.inv(p)
    print(d)
    print(np.array_equal(np.round(p @ d @ pi, 3), T))

    ### DIFFICULT SERIES OF MOVES
    # Calculating (((((F' D R' D U2)k (D' R D' F U2)k)k (R' U R' F L2)k)k (R D' F U2 D')k)k (D F' D R' U2)k)k

    k = 10**9 + 7
    orders = ["F' D R' D U2", "D' R D' F U2", "R' U R' F L2", "R D' F U2 D'", "D F' D R' U2"]
    T = mat_exp(move_mat(orders[0], moves), k)
    for order in orders[1:]:
        T = mat_exp(mat_exp(move_mat(order, moves), k) @ T, k)

    print(apply(T, M, cube.Cube()))
