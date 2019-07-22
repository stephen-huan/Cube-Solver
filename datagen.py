from cube import *
from collections import deque
import numpy as np
import sys, os
import subprocess

original_stdout = None
def disable_print():
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout.close()
    sys.stdout = original_stdout

def small_datagen(bfs_len, metric=HTM):
    data = []
    start = Cube()
    seen = {}
    q = deque([(start, [])])
    states = 0
    while q:
        states += 1
        n, moves = q.popleft()
        repr = fast_str(n.cube)
        seen[repr] = moves
        data.append((repr,moves))
        
        if bfs_len <= len(moves):
            continue

        for move in metric.moves:
            if len(moves) == 0 or move[0] != moves[-1][0]:
                child = Cube(n)
                child.turn(move)
                repr, movesp = fast_str(child.cube), moves + [move]
                if repr in seen:
                    continue
                seen[repr] = movesp
                q.append((child, movesp))

    print(states)
    return data


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

#Convert to the cube format for optimal kociemba solver
def convert_to_optimal(cubes):
    singmanes = []
    for n in cubes:
        cube = n.cube
        singman = ""
        face_dict = {cube[0][4].colors[0]:'U',cube[1][1].colors[1]:'B',cube[1][3].colors[2]:'L',cube[1][5].colors[2]:'R',cube[1][7].colors[1]:'F',cube[2][4].colors[0]:'D'}
        edge_order = [(0,7), (0,5), (0,1), (0,3), (2,7), (2,5), (2,1), (2,3), (1,8), (1,6), (1,2), (1,0)]
        corner_order = [(0,8,False), (0,2,True), (0,0,False), (0,6,True), (1,8,True), (1,6,False), (1,0,True), (1,2,False)]
        for a,b in edge_order:
            colors = ''.join(cube[a][b].colors).replace(' ', '')
            singman += colors + " "

        for a,b,switch in corner_order:
            colors = ''.join(cube[a][b].colors)
            if switch:
                colors = colors[0] + colors[2] + colors[1]        
            singman += colors + " "
        singmans.append(singman)
        #Write to file here
    return singmans

def parse_optimal_output():
    file = open('output.txt', 'r')
    lines = file.read().split("\n")
    solutions = []
    for line in lines:
        if 'q*' not in line:
            continue
        line = line[:line.index("(")]
        solutions.append(line.strip())
    #Write solutions to a new file
    print(solutions)


"""
#NOT OPTIMAL REEEEE
def solve_kociemba(n, verbose):
    cube = n.cube
    face_dict = {cube[0][4].colors[0]:'U',cube[1][1].colors[1]:'B',cube[1][3].colors[2]:'L',cube[1][5].colors[2]:'R',cube[1][7].colors[1]:'F',cube[2][4].colors[0]:'D'}
    str_rep = ""
    face_rep = [flip(list_mat(get(INT_STR, face)), FLIPPED.get(i, None)) for i, face in enumerate(n.to_face())]
    order = [0,2,1,5,3,4]
    for i in order:
        face = face_rep[i][0] + face_rep[i][1] + face_rep[i][2]
        for j in face:
            str_rep += face_dict[ORDER[COLORS.index(j)]]
    if not verbose:
        disable_print()
    from twophase.solve import Solver
    s = Solver()
    solution = s.solve(str_rep, 100)
    print(solution)
    if not verbose:
        enable_print()
"""


def save_data(filename, data, datatype=0):
    DELIM = ';'
    file = open(filename, 'w+')
    file_data = []
    for state, moves in data:
        X = state
        if datatype == 0: #Save best next move.
            if len(moves) == 0: #IDK what the Y data should be for a solved cube
                continue
            y = opposite(moves[len(moves) - 1])
        else: #Save number of moves in optimal solution
            y = str(len(moves))
        file_data.append([X,y])
    file_data = np.array(file_data)
    np.savetxt(filename, file_data)

if __name__ == "__main__":
#    data = small_datagen(2)
#    save_data('training_data.csv', data)
    cube = Cube()
#    cube.turn("U U F U U R' L F F U F' B' R L U U R U D' R L' D R' L' D D")
    cube.turn("B D B U L F L U' R B D' D F' L' L L F U R L'")
    solve_kociemba(cube, True)