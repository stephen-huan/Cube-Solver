import cube as cb

cube = cb.Cube()
cube.turn("R U2 R U R U2 R U2 R2 U' R' U2 R U' R U' R2 U' R' U2 R' U2 R2 U R2")
states, solution, seen = cb.solve(cube, metric=cb.TGEN)
print(solution)