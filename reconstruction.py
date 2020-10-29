import cube.cube as cube

# example of a reconstruction
# 41 HTM/5.44 = 7.54 TPS done while talking about railgun 
c = cube.Cube()
c.turn("L2 U B U B' L F B' L' R2 D2 L2 F2 B2 U R2 F2 U2 B2 U L") # scramble
c.turn("x2 y")                 # inspection
c.turn("L F' D' R' D")         # cross
c.turn("y U R U R' L U' L'")   # 1st pair
c.turn("U2 R' U' R U' R' U R") # 2nd pair
c.turn("y' U2 R' U' R")        # 3rd pair
c.turn("U2 R U' R' U R U' R'") # 4th pair
c.turn("U' R U R' U R U2 R'")  # OLL + PLL skip
c.turn("U'")                   # AUF
print(c)

# last 2 pairs + LL is 2gen
# what if I did it optimally?
c = cube.Cube()
c.turn("L2 U B U B' L F B' L' R2 D2 L2 F2 B2 U R2 F2 U2 B2 U L") # scramble
c.turn("x2 y")                 # inspection
c.turn("L F' D' R' D")         # cross
c.turn("y U R U R' L U' L'")   # 1st pair
c.turn("U2 R' U' R U' R' U R") # 2nd pair
c.turn("y'")
print(c)

goal = cube.Cube()
goal.turn("x2 y")
sol = cube.solve(c, target=(goal, cube.solved), metric=cube.TGEN)[1]
print(sol, len(cube.tokenize(sol)))

