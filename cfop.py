import cube as cb

def cross(cube, *args, face=cb.W): return all(cb.cubie_correct(cube, edge) for edge in zip([face]*4, cb.CWE))

def pair(cube, number=1):
    """ Only works on white cross. """
    return sum(int(cb.cubie_correct(cube, corner) and cb.cubie_correct(cube, (corner[0] + 1, corner[1]))) for corner in zip([cb.W]*4, cb.CWC)) >= number

def oll(cube, face=cb.Y): return list(set(cube.to_face()[face])) == [face]

def perform_step(cube, solution, f, name):
    temp = cb.tokenize((cb.solve(cube) if f == cb.solved else cb.IDsolve(cube, (None, f)))[1])
    solution += temp
    cube.turn(temp)
    if name:
        print(f"{name} solution: {' '.join(temp)}")

def cfop(cube, face=cb.W):
    solution = []
    p = (cube, solution)

    perform_step(*p, cross, "Cross")
    for num in range(1, 5):
        perform_step(*p, lambda cube, *args: cross(cube) and pair(cube, num), f"{num} pair")
    perform_step(*p, lambda cube, *args: cross(cube) and pair(cube, 4) and oll(cube), "OLL")
    perform_step(*p, cb.solved, "PLL")

    return " ".join(solution)

cube = cb.Cube()
# cube.turn("U B2 R' U2 F2 D2 R F2 L' B2 D2 L B2 D' F2 R D U B' R F'")
cube.turn("x' R' U R' D2 R U' R' D2 R2 x'")

# # print(cross(cube))
# cube.turn("x2 y R' F D' B' R'")
# # print(cross(cube))

# print(pair(cube))
# cube.turn("x2 y L' U' L U' R U R' U2 R U' R'")
# print(pair(cube))
# cube.turn("x2 y2 U2 R U' R' F' U' F")
# print(pair(cube))
# cube.turn("x2 y' U2 R' U R U' R' U' R")
# print(pair(cube))
# cube.turn("x2 y' U' F' U' F U' R U R'")
# print(pair(cube))

# print(oll(cube))
# cube.turn("x2 y' U2 F U R U' R' F'")
# print(oll(cube))

print(cfop(cube))
