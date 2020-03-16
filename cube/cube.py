import itertools, pickle, inspect
from collections import deque
from time import time
import cube.colors as colors
"""
Simulation of a Rubik's cube in Python.

Face names are equivalent to colors in standard orientation.
i.e. up down, front back, right left = white yellow, green blue, red orange = w y, g b, r o respectively.
WCA orientation is white top green front.
"""

### NAMED CONSTANTS ###

def inv(d): return {v: k for k, v in d.items()}

#U, D, F, B, R, L = 0, 5, 1, 4, 2, 3
ORDER = [0, 5, 1, 4, 2, 3]
W, Y, G, B, R, O = ORDER
COLORS = "WYGBRO"
INT_STR = dict(zip(ORDER + [None], COLORS + " "))
STR_INT = inv(INT_STR)
CWC, CWE = [0, 2, 8, 6], [1, 5, 7, 3]
UP, DOWN, LEFT, RIGHT = [0, 1, 2], [6, 7, 8], [0, 3, 6], [2, 5, 8]
ORIENT = {i: j//2 for j, i in enumerate(ORDER)}
FLIPPED = {R: False, B: False, Y: True}

MOVES = "UDFBRL"
COLORS_MOVE = dict(zip(COLORS, MOVES))
MOVE_COLORS = inv(COLORS_MOVE)
STR_NUM = {'': 1, '2': 2, "'": 3}
NUM_STR = inv(STR_NUM)
FACE = [G, R, B, O, W, Y] # Srikar specification
x, y, z = ORIENT[R], ORIENT[W], ORIENT[G]

PREFIX = "/Users/stephenhuan/datasets/cubing/"

### HELPER FUNCTIONS ###

def get(l, indexes): return [l[i] for i in indexes]

def multi_zip(l1, l2): return [(x, y) for x in l1 for y in l2]

def list_mat(l): return [l[3*i: 3*(i + 1)] for i in range(3)]

def mat_list(m): return list(itertools.chain(*m))

def access(l, i):
    val = l
    for j in i:
        val = val[j]
    return val

def modify(l, i, v):
    val = l
    for j in range(len(i) - 1):
        val = val[i[j]]
    val[i[-1]] = v

def cycle(l, indexes):
    start = access(l, indexes[-1])
    for i in range(len(indexes) - 1, 0, -1):
        modify(l, indexes[i], access(l, indexes[i - 1]))
    modify(l, indexes[0], start)

def mat_str(m): return "\n".join((" ".join(row) for row in m))

def join_two(s1, s2): return "\n".join((a + " "*2 + b for a, b in zip(s1.split("\n"), s2.split("\n"))))

def horz_join(*s):
    out = s[0]
    for i in range(1, len(s)):
        out = join_two(out, s[i])
    return out

def flip(m, dir):
    if dir is None: return m
    dir = (lambda i, j: (2 - i, j)) if dir else (lambda i, j: (i, 2 - j))
    temp = [[None]*3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            x, y = dir(i, j)
            temp[x][y] = m[i][j]
    return temp

def tokenize(moves): return moves.split() if type(moves) is str else moves

def opposite(move): return move[0] + {"'": "", "2":"2"}.get(move[-1], "'")

def inverse(moves): return " ".join(reversed(list(map(opposite, tokenize(moves)))))

def rotate(orient, dir):
    indexes = [(i,) for i, c in enumerate(orient) if ORIENT[c] != dir]
    i, j = (-1, -2) if dir != z else (0, 1)
    i, j = indexes[i][0], indexes[j][0]
    cycle(orient, indexes)
    cycle(orient, indexes)
    orient[i], orient[j] = orient[j], orient[i]
    return orient

def rotation(moves):
    """ Orientation of the cube is given by two numbers: top color and front color.
    6 top colors * 4 front colors / top color = 24 possible orientations
    Human FMC trick is used: no matter the orientation, turning a color is equivalent to
    the move that is associated with that color. """
    orient = ORDER.copy()
    rot = dict(zip("xyz", (x, y, z)))
    new = []
    for move in tokenize(moves):
        move, number = move[0], move[1:] if len(move) > 1 else ""
        if move in rot:
            for i in range(STR_NUM[number]):
                orient = rotate(orient, rot[move])
        else:
            new.append(COLORS_MOVE[INT_STR[orient[ORDER.index(STR_INT[MOVE_COLORS[move]])]]] + number)
    return " ".join(new)

### MAIN CLASSES ###


class Metric:

    def __init__(self, moves): self.moves = set(moves)

    def __str__(self): return " ".join(sorted(self.moves))


class Cubie:

    def __init__(self, *colors): self.colors = list(colors) #up/down, front/back, left/right

    def __str__(self): return "".join((INT_STR[c] for c in self.colors))

    def rotate(self, dir):
        i, j = {0, 1, 2} - {dir}
        self.colors[i], self.colors[j] = self.colors[j], self.colors[i]


### CUBING SPECIFIC THINGS ###

MOVES = "UDFBRL"
HTM = Metric(mat_list(((move, move + "'", move + "2") for move in MOVES)))
QTM = Metric(mat_list((move, move + "'") for move in MOVES))
TGEN = Metric(mat_list(((move, move + "'", move + "2") for move in "RU")))

def str_cubies(cube):
    return [[Cubie([lambda i, j: cube[0][i][j], lambda i, j: None, lambda i, j: cube[5][2 - i][j]][layer](i, j),
                    None if i == 1 else cube[4 if i == 0 else 2][layer][2 - i + (-1 if i == 0 else 1)*j],
                    None if j == 1 else cube[j + 1][layer][i if j == 0 else 2 - i])
             for i in range(3) for j in range(3)] for layer in range(3)]

def get_solved_cube(): return [[Cubie([W, None, Y][layer], [B, None, G][i], [O, None, R][j]) for i in range(3) for j in range(3)] for layer in range(3)]

def fast_str(m): return  "".join(map(str, mat_list(m)))

def faster_rep(m):
    string = fast_str(m)
    bin_string = ''.join([bin(ORDER[COLORS.index(i)] if i in COLORS else 6)[2:] for i in string])
    return int(bin_string, 2)

def solved(cube, *args): return fast_str(cube.cube) == fast_str(get_solved_cube())

def cubie_correct(cube, cubie):
    intersect = [face for face in ORDER if cubie in cube.get_layer(face)]
    return all(c == intersect[i] for i, c in enumerate(filter(lambda c: c is not None, access(cube.cube, cubie).colors)))

class Cube:

    def __init__(self, other=None, init_cube=True):
        #WGROBY, standard color scheme
        #layer by layer starting from the top; top - down left - right
        if init_cube:
            self.cube = get_solved_cube() if other is None else [[Cubie(*cubie.colors) for cubie in layer] for layer in other.cube]
        self.turns = dict(zip("UDFBRL", ORDER))
        self.layers = {0: self.get_ud_layer, 1: self.get_fb_layer, 2:self.get_lr_layer}

    def __str__(self): return colors.color(self.to_str())

    def to_str(self):
        cube = [flip(list_mat(get(INT_STR, face)), FLIPPED.get(i, None)) for i, face in enumerate(self.to_face())]
        out = horz_join((" "*5 + "\n")*3, mat_str(cube[0]))
        out += "\n" + horz_join(*map(mat_str, [cube[face] for face in [O, G, R, B]]))
        out += "\n" + horz_join((" "*5 + "\n")*3, mat_str(cube[-1]))
        return out

    def export(self, fname):
        with open(fname, "w") as f:
            f.write(self.to_str())

    def get_fb_layer(self, row): return multi_zip(range(3), range(3*row, 3*(row + 1)))

    def get_lr_layer(self, col): return multi_zip(range(3), range(col, 9, 3))

    def get_ud_layer(self, layer): return list(zip([layer]*9, range(9)))

    def get_layer(self, face):

        return self.layers[ORIENT[face]](0 if face in [W, B, O] else 2)

    def to_face(self, order=range(6)):
        return [[cubie.colors[min(face, 5 - face)] for cubie in (access(self.cube, i) for i in self.get_layer(face))] for face in order]

    def move(self, dir):
        layer = self.get_layer(dir)

        cycle(self.cube, get(layer, CWC))
        cycle(self.cube, get(layer, CWE))

        for cubie in layer:
            access(self.cube, cubie).rotate(ORIENT[dir])

    def turn(self, moves):
        for move in tokenize(rotation(moves)):
            move, number = move[0], move[1:] if len(move) > 1 else 1
            number = 3 if number == "'" else int(number)
            for i in range(4 - number if self.turns[move] in FLIPPED else number):
                self.move(self.turns[move])

def sticker_move_dict():
    reverse = lambda arr: list(reversed(arr))
    turn_dict = {}
    turn_dict['R'] = {W:RIGHT, B:reverse(LEFT), Y:RIGHT, G:RIGHT, "order":[W,B,Y,G], "face":R}
    turn_dict['L'] = {W:LEFT, B:reverse(RIGHT), Y:LEFT, G:LEFT, "order":[W,G,Y,B], "face":O}
    turn_dict['U'] = {G:UP, O:UP, B:UP, R:UP, "order":[G,O,B,R], "face":W}
    turn_dict['D'] = {G:DOWN, O:DOWN, B:DOWN, R:DOWN, "order":[G,R,B,O], "face":Y}
    turn_dict['F'] = {W:reverse(DOWN), R:reverse(LEFT), Y:UP, O:RIGHT, "order":[W,R,Y,O], "face":G}
    turn_dict['B'] = {W:reverse(UP), R:reverse(RIGHT), Y:DOWN, O:LEFT, "order":[W,O,Y,R], "face":B}

    move_dict = {}
    for move in turn_dict:
        turn = turn_dict[move]
        seq1,seq2,seq3 = [],[],[]
        for side in turn["order"]:
            stickers = turn[side]
            seq1.append([(side, int(sticker/3), sticker % 3) for sticker in stickers])

        for sticker in CWC:
            seq2.append([(turn["face"], int(sticker/3), sticker % 3)])

        for sticker in CWE:
            seq3.append([(turn["face"], int(sticker/3), sticker % 3)])

        move_dict[move] = [seq1, seq2, seq3]
    return move_dict


class StickerCube:

    def __init__(self, other=None):
        #Face order is WGROBY, standard color scheme
        #cube is a 2D array (6x3x3)
        self.cube = self.get_solved_cube() if other is None else [[[k for k in j] for j in i] for i in other.cube]
        self.turns = dict(zip("UDFBRL", ORDER))
        self.move_dict = sticker_move_dict()

    def __str__(self): return colors.color(self.to_str())

    def to_str(self):
        cube = self.to_face()

        out = horz_join((" "*5 + "\n")*3, mat_str(cube[0]))
        out += "\n" + horz_join(*map(mat_str, [cube[face] for face in [O, G, R, B]]))
        out += "\n" + horz_join((" "*5 + "\n")*3, mat_str(cube[-1]))
        return out

    def to_face(self):
        return [[[INT_STR[i] for i in j] for j in k] for k in self.cube]

    def get_solved_cube(self):
        return [[[i for b in range(3)] for a in range(3)] for i in range(6)]

    def export(self, fname):
        with open(fname, "w") as f:
            f.write(self.to_str())

    def overlay(self, curr, want):
        for j in range(len(curr)):
            temp1 = curr[j]
            temp2 = want[j]
            self.cube[temp1[0]][temp1[1]][temp1[2]] = self.cube[temp2[0]][temp2[1]][temp2[2]]

    def follow_seq(self, seq, diff):
        i = 0
        temp = [self.cube[temp[0]][temp[1]][temp[2]] for temp in seq[i]]
        first = True
        length = len(seq)
        start = time()
        while i != 0 or first:
            curr = seq[i]
            want = seq[(i + diff) % length]
            first = False
            self.overlay(curr, want)
            i += diff
            i %= length

        want = seq[(i - diff) % length]
        for j in range(len(temp)):
            temp1 = want[j]
            self.cube[temp1[0]][temp1[1]][temp1[2]] = temp[j]
        end = time() - start
        return end

    def move(self, move, num):
        diff = 1 if num == 3 else -1
        seqs = self.move_dict[move]
        for seq in seqs:
            self.follow_seq(seq, diff)
        if num == 2:
            for seq in seqs:
                self.follow_seq(seq, diff)

    def turn(self, moves):
        for move in tokenize(moves):
            move, number = move[0], move[1:] if len(move) > 1 else 1
            number = 3 if number == "'" else int(number)
            self.move(move, number)

### MORE STUFF ###

def solve(start, target=(Cube(), solved), metric=HTM, cache={}):
    goal, evaluate = target

    seen = [{}, {}]
    q = [deque([(start, [])]), deque([(goal, [])])]
    states = 0
    poss = 1 if goal is None else 2

    def goal_test(node, repr, moves):
        if repr in cache:
            return states, " ".join(moves) + " " + inverse(cache[repr]), seen

        if repr in seen[i ^ 1] if goal is not None else evaluate(node, moves):
            if goal is None: return states, moves, seen
            prefix, suffix = (moves, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], moves)
            return states, " ".join(prefix) + " " + inverse(suffix), seen

    while len(q[0]) > 0 or len(q[1]) > 0:
        for i in range(poss):
            n, moves = q[i].popleft()

            val = goal_test(n, fast_str(n.cube), moves)
            if val is not None: return val

            for move in metric.moves:
                if len(moves) == 0 or move[0] != moves[-1][0]:
                    states += 1
                    child = Cube(n)
                    child.turn(move)
                    repr, movesp = fast_str(child.cube), moves + [move]

                    val = goal_test(child, repr, movesp)
                    if val is not None: return val

                    if repr not in seen[i]:
                        seen[i][repr] = movesp
                        q[i].append((child, movesp))

# TODO: make bidirectional
def IDdfs(start, target, metric, depth, filename):
    goal, evaluate = target

    seen = [{}, {}]
    stk = [(Cube(start), set(), [])], [(goal, set(), [])]
    states = 0
    poss = 1 if goal is None else 2

    f = open(filename, "a")

    def goal_test(node, repr, moves):
        if repr in seen[i ^ 1] if goal is not None else evaluate(node, moves):
            if goal is None: return states, moves
            prefix, suffix = (moves, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], moves)
            return states, " ".join(prefix) + " " + inverse(suffix), seen

    while len(stk[0]) > 0: #or len(stk[1]) > 0:
        for i in range(poss):
            n, path, moves = stk[i].pop()

            val = goal_test(n, fast_str(n.cube), moves)
            if val is not None: return val

            children = False
            for move in metric.moves:
                if len(moves) == 0 or move[0] != moves[-1][0]:
                    states += 1
                    child = Cube(n)
                    child.turn(move)
                    repr, movesp = fast_str(child.cube), moves + [move]

                    val = goal_test(child, repr, movesp)
                    if val is not None: return val

                    if len(movesp) == depth:
                        f.write(f"{repr}: {' '.join(movesp)}\n")

                    if repr not in path and len(path) < depth:
                        children, last = True, move
                        stk[i].append((child, path | {repr}, movesp))
    f.close()

def IDsolve(start, target=(Cube(), solved), metric=HTM, maxdepth=float("INF"), filename="temp.pickle"):
    rtn, depth = None, 0
    while rtn is None and depth <= maxdepth:
        rtn = IDdfs(start, target, metric, depth, filename)
        # print(depth)
        depth += 1
    return rtn

def import_cube(fname):
    with open(fname) as f:
        data = [STR_INT[ch] for ch in f.read() if ch != " " and ch != "\n"]

    cube = [list_mat(data[:9])] + [[data[i:i + 3] for i in range(j, 43, 12)] for j in range(9, 21, 3)] + [list_mat(data[-9:])]

    obj = Cube()
    obj.cube = str_cubies(cube)
    return obj

def speedtest():
    start = time()
    cube = StickerCube()
    s1, s2, s3 = cube.move_dict["R"]
    print(len(s1), len(s2), len(s3))
    moves = "R U R' U'"
    for i in range(10000):
        cube.follow_seq(s1, 1)
        cube.follow_seq(s2, 1)
        cube.follow_seq(s3, 1)
    print("Sticker Turn Time:", time()-start)


if __name__ == "__main__":
    speedtest()
#    cube = StickerCube()
#    cube.turn("R U R' L F D' U' F L' B2 R' U2 L")
#    print(cube,"\n\n")
#    cube2 = Cube()
#    cube2.turn("R U R' L F D' U' F L' B2 R' U2 L")
#    print(cube2)

""" if __name__ == "__main__":
    with open(f"{PREFIX}cache.pickle", "rb") as f:
        cache = pickle.load(f)

    # cube = import_cube("test.txt")
    cube = Cube()
    cube.turn("R U' R U R U R U' R' U' R2")
    print(cube)
    # states, alg, seen = solve(cube, (Cube(), solved), HTM)
    states, alg, seen = solve(cube, (None, solved), HTM, cache)
    print(states, alg, len(tokenize(alg)))
 """
