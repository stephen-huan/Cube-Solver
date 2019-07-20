import numpy as np
import random
import cube

"""
https://en.wikipedia.org/wiki/Generalized_inverse
https://en.wikipedia.org/wiki/Inverse_element#Matrices
https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse
"""

a = [[1, 2],
     [3, 4]]
b = [[2, 1],
     [3, 4]]
# b = [[2, 1],
#      [4, 3]]
I = [[1, 0],
     [0, 1]
    ]

I = np.array(I)

ap = np.linalg.inv(a)
swap = ap @ b

# print(swap)
# print(a @ swap)
# print(a @ swap @ swap)

### CUBE ###

solved = np.array([[i]*9 for i in range(6)])
solvedp = np.array([[0, 0, 5, 0, 0, 5, 0, 0, 5],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [4, 2, 2, 4, 2, 2, 4, 2, 2],
                   [3, 3, 3, 3, 3, 3, 3, 3, 3],
                   [4, 4, 0, 4, 4, 0, 4, 4, 0],
                   [5, 5, 2, 5, 5, 2, 5, 5, 2]])

solvedd = np.array([[0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]])

checker = np.array([[0, 2, 0, 2, 0, 2, 0, 2, 0],
                    [1, 3, 1, 3, 1, 3, 1, 3, 1],
                    [2, 0, 2, 0, 2, 0, 2, 0, 2],
                    [3, 1, 3, 1, 3, 1, 3, 1, 3],
                    [4, 5, 4, 5, 4, 5, 4, 5, 4],
                    [5, 4, 5, 4, 5, 4, 5, 4, 5]])

checkerr = np.array([[0, 2, 5, 2, 0, 4, 0, 2, 5],
                     [1, 3, 1, 3, 1, 3, 1, 3, 1],
                     [4, 0, 2, 5, 2, 0, 4, 0, 2],
                     [3, 1, 3, 1, 3, 1, 3, 1, 3],
                     [4, 5, 0, 5, 4, 2, 4, 5, 0],
                     [5, 4, 2, 4, 5, 0, 5, 4, 2]])

def transform(mapping, m):
    new = [[0]*9 for i in range(6)]
    for i in range(6):
        for j in range(9):
            x, y = mapping[(i, j)]
            new[i][j] = m[x][y]
    return np.array(new)

def gen_random(m=solved):
    indexes = [(i, j) for i in range(6) for j in range(9)]
    trans = {}
    for i in range(6):
        for j in range(9):
            trans[(i, j)] = random.choice(indexes)
            indexes.remove(trans[(i, j)])
    return transform(trans, m), trans

def inversable(m, tol=2):
    m = np.array(m)
    if np.linalg.matrix_rank(m) == 6:
        return round(np.linalg.det(m.T @ m), tol) != 0, round(np.linalg.det(m @ m.T), tol) != 0
    return (False,)*2

def diff(m1, m2):
    return sum(1 for i in range(6) for j in range(9) if m1[i][j] != m2[i][j])

def rdiff(c):
    m1 = c.to_face()
    c.turn("R")
    m2 = c.to_face()
    c.turn("R'")

    return diff(m1, m2)

c = cube.Cube()

states, alg = cube.solve(c, (None, lambda c: rdiff(c) >= 20), cube.HTM)
c.turn(alg)
# c.turn("B' D' F2")

print(rdiff(c))
print(inversable(c.to_face()))

a = np.array(c.to_face())
c.turn("R")
ap = np.array(c.to_face())

ar = a.T @ np.linalg.inv(a @ a.T)
R = ar @ ap
print(a @ R)

# print(ap)

# I = np.identity(6)
# new, trans = gen_random(solved)
# a = new
#
# print(inversable(a))
#
# # al = np.linalg.inv(a.T @ a) @ a.T
# # print(np.linalg.inv(a.T @ a) @ a.T @ a )
# # print(al @ a)
#
# solvedp = transform(trans, solvedp)
# print(solvedp)
#
# ar = a.T @ np.linalg.inv(a @ a.T)
# # print(a @ ar)
# # R = solvedp @ ar
# # print(R @ a)
#
# R = ar @ solvedp
# print(a)

# m = np.linalg.pinv(a)
# print(np.allclose(a, np.dot(a, np.dot(m, a))), np.allclose(m, np.dot(m, np.dot(a, m))))
# R = m @ solvedp
# print(solved @ R)
# x = np.linalg.lstsq(solved, solvedp)[0]
# print(solved @ x)
