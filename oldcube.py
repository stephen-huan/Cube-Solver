def rowstr(l): return " ".join(map(str, l))

class Cube:

    def __init__(self):
        #WGRBOY, standard color scheme
        self.cube = [[[i]*3 for j in range(3)] for i in range(6)]
        self.neigh = [[1, 2, 3, 4],
                      [0, 2, 4, 5],
                      [0, 1, 3, 5],
                      [0, 2, 4, 5],
                      [0, 1, 3, 5],
                      [1, 2, 3, 4]]

    def __str__(self):
        out = ""
        cube = [[["wgrboy"[row[i]] for i in range(3)] for row in face] for face in self.cube]
        for row in cube[0]:
            out += " "*7 + rowstr(row) + "\n"
        for i in range(3):
            for j in [4, 1, 2, 3]:
                out += rowstr(cube[j][i]) + "  "
            out += "\n"
        for row in cube[5]:
            out += " "*7 + rowstr(row) + "\n"
        return out[:-1]

    def move(self, i):
        face = self.cube[i]
        #print(face)

        face[0][0], face[0][-1], face[-1][0], face[-1][-1] = face[0][0], face[0][-1], face[-1][0], face[-1][-1]]
        face[0][1], face[1][0], face[1][-1], face[-1][1] = face[0][1], face[1][0], face[1][-1], face[-1][1]]

        self.cube[self.neigh[i][0]][i][0]
        self.cube[self.neigh[i][0]][i][0]
        self.cube[self.neigh[i][0]][i][0]
        self.cube[self.neigh[i][0]][i][0]
        # num = i
        # if i == 5:
        #     num = -1
        #
        # band = [self.cube[j][num] for j in self.neigh[i]]
        #
        # new = rotate(band)
        # for j in range(4):
        #     self.cube[self.neigh[i][j]][num] = new[j]

cube = Cube()

print(cube)

"""
Code graveyard

def cycle(l, js):
    start = l[js[-1]]
    for i in range(len(js) - 1, 0, -1):
        l[js[i]] = l[js[i - 1]]
    l[js[0]] = start

if dir == 0:
    self.c1, self.c2, self.c3 = self.c2, self.c1, self.c3
elif dir == 1:
    self.c1, self.c2, self.c3 = self.c3, self.c2, self.c1
else:
    self.c1, self.c2, self.c3 = self.c1, self.c3, self.c2

turns = {k: (v if v[0] not in FLIPPED else (v[0], v[1] + 2)) for k, v in zip("UDFBRL", zip(ORDER, [1]*6))}

def get_fb_layer(self, row):
    return mat_list([self.cube[layer][3*row:3*(row + 1)] for layer in range(3)])
    return [(layer, i) for layer in range(3) for i in range(3*row, 3*(row + 1))]

def get_lr_layer(self, col):
    return [self.cube[layer][i] for layer in range(3) for i in range(col, 9, 3)]
    return [(layer, i) for layer in range(3) for i in range(col, 9, 3)]

def get_ud_layer(self, layer):
    return self.cube[layer]
    return list(zip([layer]*9, range(9)))

def get_layer(self, face):
    layer = {W: self.get_ud_layer(0),
             Y: self.get_ud_layer(2),
             G: self.get_fb_layer(2),
             B: self.get_fb_layer(0),
             R: self.get_lr_layer(2),
             O: self.get_lr_layer(0)
            }[face]
    #return [cubie.colors[min(face, 5 - face)] for cubie in layer]
    #return [cubie.colors[min(face, 5 - face)] for cubie in map(lambda i: self.cube[i[0]][i[1]], layer)]
    return layer

def to_face(self): #return [cube.get_layer(face) for face in range(6)]
    #return [[cubie.colors[min(face, 5 - face)] for cubie in map(lambda i: access(self.cube, i), cube.get_layer(face))] for face in range(6)]
    return [[cubie.colors[min(face, 5 - face)] for cubie in (access(self.cube, i) for i in cube.get_layer(face))] for face in range(6)]

def opposite(move):
    if move[-1] == "'":
        return move[:-1]
    if move[-1] == "2":
        return move
    return move + "'"

def solve(start, target=(Cube(), solved), metric=HTM):
    goal, evaluate = target

    seen = {}
    q = deque([(start, [])])
    states = 0
    while len(q) > 0:
        n, moves = q.popleft()
        repr = fast_str(n.cube)
        seen[repr] = moves
        if evaluate(n):
            return states, moves
        for move in metric.moves:
            states += 1
            child = Cube(n)
            child.turn(move)
            if fast_str(child.cube) not in seen:
                q.append((child, moves + [move]))

def get_solved_cube():
    return [[Cubie(W, B, O), Cubie(W, B, None), Cubie(W, B, R),
             Cubie(W, None, O), Cubie(W, None, None), Cubie(W, None, R),
             Cubie(W, G, O), Cubie(W, G, None), Cubie(W, G, R)
            ],
            [Cubie(None, B, O), Cubie(None, B, None), Cubie(None, B, R),
             Cubie(None, None, O), Cubie(None, None, None), Cubie(None, None, R),
             Cubie(None, G, O), Cubie(None, G, None), Cubie(None, G, R)
            ],
            [Cubie(Y, B, O), Cubie(Y, B, None), Cubie(Y, B, R),
             Cubie(Y, None, O), Cubie(Y, None, None), Cubie(Y, None, R),
             Cubie(Y, G, O), Cubie(Y, G, None), Cubie(Y, G, R)
            ]
           ]

def parse_result(repr, other, states, moves):
    prefix, suffix = (moves, other[repr]) if i == 0 else (other[repr], moves)
    return states, " ".join(prefix) + " " + inverse(suffix)

def goal_test(node, other, goal, evaluate, *args):
    repr = fast_str(node.cube)
    if repr in other if goal is not None else evaluate(node):
        if goal is None: return args
        return parse_result(repr, other, *args)

def solve(start, target=(Cube(), solved), metric=HTM):
    goal, evaluate = target

    seen = [{}, {}]
    q = [deque([(start, [], "*")]), deque([(goal, [], "*")])]
    states = 0
    poss = 1 if goal is None else 2

    while len(q[0]) > 0 or len(q[1]) > 0:
        for i in range(poss):
            n, moves, last = q[i].popleft()
            #n.turn(moves)
            repr = fast_str(n.cube)
            seen[i][repr] = moves
            if repr in seen[i ^ 1] if goal is not None else evaluate(n):
                if goal is None: return states, moves

                prefix, suffix = (moves, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], moves)
                return states, " ".join(prefix) + " " + inverse(suffix)
            for move in metric.moves:
                if move[0] != last[0]:
                    states += 1

                    # child = n
                    # child.turn(move)
                    child = Cube(n)
                    child.turn(move)
                    repr, movesp = fast_str(child.cube), moves + [move]

                    if repr not in seen[i]:
                        seen[i][repr] = movesp
                        q[i].append((child, movesp, move))

                    #     if repr in seen[i ^ 1] if goal is not None else evaluate(child):
                    #         if goal is None: return states, movesp
                    #         prefix, suffix = (movesp, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], movesp)
                    #         return states, " ".join(prefix) + " " + inverse(suffix)

                    # child.turn(inverse(move))

            # n.turn(inverse(moves))

"""
