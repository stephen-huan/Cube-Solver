from cube import *

##LEGEND:
#Assume normal solved state (Green facing you, White on top, Red on right)
#Corner Positions: 0 = WBO, 1 = WBR, 2 = WGO, 3 = WGR, 4 = YBO, 5 = YBR, 6 = YGO, 7 = YGR
#Corner Orientations: 0 = W/Y on bottom/top, 1 = B/G on bottom/top, 2 = R/O on bottom/top
#Edge color hierarchy: W/Y, then B/G, then R/O
#Edge orientation hierarchy: Top/Bottom, then Front/Back, then Left/Right
#Edge Positions: 0 = WB, 1 = WR, 2 = WG, 3 = WO, 4 = BO, 5 = BR, 6 = GO, 7 = GO, 8 = YB, 9 = YR, 10 = YG, 11 = YO
#Edge Orientations: 0 = Higher color hierarchy facing higher orientation hierarchy, 1 = Opposite of 0

HEIRARCHY = 'WYBGRO'

corner_map = {
    'WBO': 0,
    'WBR': 1,
    'WGO': 2,
    'WGR': 3,
    'YBO': 4,
    'YBR': 5,
    'YGO': 6,
    'YGR': 7,
}

corner_map_inverse = inv(corner_map)
corner_indices = [(0,0), (0,2), (0,6), (0,8), (2,0), (2,2), (2,6), (2,8)]

edge_map = {
    'WB': 0,
    'WO': 1,
    'WR': 2,
    'WG': 3,
    'BO': 4,
    'BR': 5,
    'GO': 6,
    'GR': 7,
    'YB': 8,
    'YO': 9,
    'YR': 10,
    'YG': 11,
}

edge_map_inverse = inv(edge_map)
edge_indices = [(0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,6), (1,8), (2,1), (2,3), (2,5), (2,7)]
edge_gap_positions = [2, 1, 1, 2, 0, 0, 0, 0, 2, 1, 1, 2]

def onehot_vector(val, maxval):
    return [1 if i == val else 0 for i in range(maxval)]

def vectorize(n):
    cube = n.cube
    corner_colors = [cube[a][b] for a,b in corner_indices]#cube[0][0], cube[0][2], cube[0][6], cube[0][8], cube[2][0], cube[2][2], cube[2][6], cube[2][8]]
    corner_locations = [corner_map[''.join(sorted(str(i), key = lambda x: HEIRARCHY.index(x)))] for i in corner_colors]
    corner_orientations = [int(HEIRARCHY.index(str(i)[0])/2) for i in corner_colors]
    vector_corner = [onehot_vector(pos,8) + (onehot_vector(ori,3)) for (pos,ori) in zip(corner_locations, corner_orientations)]

    edge_colors = [cube[a][b] for a,b in edge_indices]
    edge_locations = [edge_map[''.join(sorted(str(i).replace(' ',''), key = lambda x: HEIRARCHY.index(x)))] for i in edge_colors]
    edge_orientations = [0 if HEIRARCHY.index(str(i).replace(' ','')[0]) < HEIRARCHY.index(str(i).replace(' ','')[1]) else 1 for i in edge_colors]
    vector_edge = [onehot_vector(pos,12) + (onehot_vector(ori,2)) for (pos,ori) in zip(edge_locations, edge_orientations)]

    vector = vector_corner + vector_edge
    vector_str = ''.join(str(digit) for innerlist in vector for digit in innerlist)
    return vector_str

def unvectorize(vec):
    #Initialize cube and set middle piece cubies
    cube = [[None for i in range(9)] for j in range(3)]
    cube[1][4] = Cubie(None, None, None)
    cube[0][4] = Cubie(W, None, None)
    cube[1][1] = Cubie(None, B, None)
    cube[1][3] = Cubie(None, None, O)
    cube[1][5] = Cubie(None, None, R)
    cube[1][7] = Cubie(None, G, None)
    cube[2][4] = Cubie(Y, None, None)
    
    for i in range(8):
        corner_pos, corner_ori = vec[i*11:i*11+8].index('1'), vec[i*11+8:i*11+11].index('1')
        corner_str = corner_map_inverse[corner_pos]
        for j in range(corner_ori):
            corner_str = corner_str[1:] + corner_str[0]
        cubie = Cubie(*[ORDER[COLORS.index(i)] for i in corner_str])
        cube[corner_indices[i][0]][corner_indices[i][1]] = cubie
        print(cubie, corner_indices[i])

    for i in range(12):
        edge_pos, edge_ori = vec[i*14+88:i*14+100].index('1'), vec[i*14+100:i*14+102].index('1')
        edge_str = edge_map_inverse[edge_pos]
        if edge_ori == 1:
            edge_str = edge_str[::-1]
        cubie_arr = []
        gap_index = edge_gap_positions[i]
        temp = 0
        for j in range(3):
            if j == gap_index:
                cubie_arr.append(None)
            else:
                cubie_arr.append(ORDER[COLORS.index(edge_str[temp])])
                temp += 1
        cubie = Cubie(*cubie_arr)
        cube[edge_indices[i][0]][edge_indices[i][1]] = cubie
        
    ret = Cube()
    ret.cube = cube
    return ret

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
    
cube = Cube()
cube.turn("R")
print(cube)
vector = vectorize(cube)
print(vector)
cube1 = unvectorize(vector)
print(cube1)