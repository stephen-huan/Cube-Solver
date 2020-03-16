import numpy as np
import random
import cube

"""
https://en.wikipedia.org/wiki/Generalized_inverse
https://en.wikipedia.org/wiki/Inverse_element#Matrices
https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse
"""

### MATH EXPERIMENTS ###

"""
# Generating a swap for a square matrix

a = [[1, 2],
     [3, 4]]
# b = [[2, 1],
#      [3, 4]]
b = [[2, 1],
     [4, 3]]
I = [[1, 0],
     [0, 1]
    ]

I = np.array(I)

ap = np.linalg.inv(a)
swap = ap @ b

print(swap)
print(a @ swap)
print(a @ swap @ swap)
"""

def pad(m, v=1):
    r, c = len(m), len(m[0])
    if r > c:
        m = [list(row) + [v]*(r - c) for row in m]
        return np.array(m)
    else:
        for i in range(c - r):
            m = np.append(m, np.array([[v]*c]), axis=0)
        return m

# more rows then columns
a = [[1, 2],
     [3, 4],
     [1, 1]]
b = [[2, 1],
     [4, 3],
     [1, 1]]

a, b = pad(a), pad(b)

ap = np.linalg.inv(a)
swap = ap @ b

# print(swap)
# print(a @ swap)
# print(a @ swap @ swap)

# more columns then rows
a = [[1, 2, 1],
     [3, 4, 1]
    ]
b = [[2, 1, 1],
     [4, 3, 1]
    ]

a, b = pad(a), pad(b)

ap = np.linalg.inv(a)
swap = ap @ b

# print(swap)
# print(a @ swap)
# print(a @ swap @ swap)
# exit()

# rotation
a = [[1, 2, 1],
     [3, 4, 1]
    ]
b = [[2, 1, 1],
     [4, 3, 1]
    ]
a, b = pad(a), pad(b)

ap = np.linalg.inv(a)
hswap = ap @ b
# print(hswap)
# print(a @ hswap)
# print(a @ hswap @ hswap)

a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
# N! possible matricies of this nature
T = [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1]]
T = [[1, 0, 0],
     [0, 0, 1],
     [0, 1, 0]]
T = [[0, 1, 0],
     [1, 0, 0],
     [0, 0, 1]]
T = [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]]
T = [[0, 0, 1],
     [0, 1, 0],
     [1, 0, 0]]
T = [[0, 1, 0],
     [0, 0, 1],
     [1, 0, 0]]

# a = np.array(a)
# print(a)
# print(a @ T)
# exit()

# print(([[1 + i + j*9 for i in range(9)] for j in range(9)]))
a = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
     [10, 11, 12, 13, 14, 15, 16, 17, 18],
     [19, 20, 21, 22, 23, 24, 25, 26, 27],
     [28, 29, 30, 31, 32, 33, 34, 35, 36],
     [37, 38, 39, 40, 41, 42, 43, 44, 45],
     [46, 47, 48, 49, 50, 51, 52, 53, 54],
     [55, 56, 57, 58, 59, 60, 61, 62, 63],
     [64, 65, 66, 67, 68, 69, 70, 71, 72],
     [73, 74, 75, 76, 77, 78, 79, 80, 81]
    ]
b = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
     [10, 11, 12, 13, 14, 15, 16, 17, 18],
     [19, 20, 21, 22, 23, 24, 25, 26, 27],
     [28, 29, 30, 31, 32, 33, 34, 35, 36],
     [37, 38, 39, 40, 41, 42, 43, 44, 45],
     [46, 47, 48, 49, 50, 51, 52, 53, 54],
     [55, 56, 57, 58, 59, 60, 61, 62, 63],
     [64, 65, 66, 67, 68, 69, 70, 71, 72],
     [73, 74, 75, 76, 77, 78, 79, 80, 81]
    ]

a = np.array(a)

ap = np.linalg.inv(a)
swap = ap @ b

print(swap)
print(a @ swap)
print(a @ swap @ swap)
exit()

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

def import_cube(data):
    c = [cube.list_mat(data[:9])] + [[data[i:i + 3] for i in range(j, 43, 12)] for j in range(9, 21, 3)] + [cube.list_mat(data[-9:])]

    obj = cube.Cube()
    obj.cube = cube.str_cubies(c)
    return obj

# ids = [[i + j*9 for i in range(9)] for j in range(6)]
ids = [i for i in range(54)]
c = import_cube(ids)
# c = cube.Cube()
print(np.array(c.to_face()))

# states, alg, seen = cube.solve(c, (None, lambda c, *args: rdiff(c) >= 20), cube.HTM)
# c.turn(alg)
c.turn("B' D' F2")
print(rdiff(c))

def cube_transform(c):
    a = np.array(c.to_face())
    a = a.T
    a = a + 2
    a = pad(a, 1)
    return a

a = cube_transform(c)
c.turn("R")
ar = cube_transform(c)

ap = np.linalg.inv(a)
R = ap @ ar

print(a)
print(ap)
print(ar)

print(R)


"""
# Psuedo-inverses

print(inversable(c.to_face()))

a = np.array(c.to_face())
c.turn("R")
ap = np.array(c.to_face())

ar = a.T @ np.linalg.inv(a @ a.T)
R = ar @ ap
print(a @ R)
"""


"""
# Archive

print(ap)

I = np.identity(6)
new, trans = gen_random(solved)
a = new

print(inversable(a))

# al = np.linalg.inv(a.T @ a) @ a.T
# print(np.linalg.inv(a.T @ a) @ a.T @ a )
# print(al @ a)

solvedp = transform(trans, solvedp)
print(solvedp)

ar = a.T @ np.linalg.inv(a @ a.T)
# print(a @ ar)
# R = solvedp @ ar
# print(R @ a)

R = ar @ solvedp
print(a)

m = np.linalg.pinv(a)
print(np.allclose(a, np.dot(a, np.dot(m, a))), np.allclose(m, np.dot(m, np.dot(a, m))))
R = m @ solvedp
print(solved @ R)
x = np.linalg.lstsq(solved, solvedp)[0]
print(solved @ x)
"""
