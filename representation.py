import cube as cb
import numpy as np

"""
LEGEND:
Assume normal solved state (Green facing you, White on top, Red on right)
Corner Positions: 0 = WBO, 1 = WBR, 2 = WGO, 3 = WGR, 4 = YBO, 5 = YBR, 6 = YGO, 7 = YGR
Corner Orientations: 0 = W/Y on bottom/top, 1 = B/G on bottom/top, 2 = R/O on bottom/top
Edge color hierarchy: W/Y, then B/G, then R/O
Edge orientation hierarchy: Top/Bottom, then Front/Back, then Left/Right
Edge Positions: 0 = WB, 1 = WR, 2 = WG, 3 = WO, 4 = BO, 5 = BR, 6 = GO, 7 = GO, 8 = YB, 9 = YR, 10 = YG, 11 = YO
Edge Orientations: 0 = Higher color hierarchy facing higher orientation hierarchy, 1 = Opposite of 0
"""

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

corner_map_inverse = cb.inv(corner_map)
corner_indices = [(0, 0), (0, 2), (0, 6), (0, 8), (2, 0), (2, 2), (2, 6), (2, 8)]

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

edge_map_inverse = cb.inv(edge_map)
edge_indices = [(0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,6), (1,8), (2,1), (2,3), (2,5), (2,7)]
edge_gap_positions = [2, 1, 1, 2, 0, 0, 0, 0, 2, 1, 1, 2]

def edge_orient(edge):
    edge = str(edge).replace(" ", "")
    return int(cb.COLORS.index(edge[0]) > cb.COLORS.index(edge[1]))

def onehot_vector(index, length):
    l = [0]*length
    l[index] = 1
    return l

def vectorize(n):
    vector = []
    for piece_type in [(corner_indices, corner_map, 3), (edge_indices, edge_map, 2)]:
        piece_indicies, piece_map, poss = piece_type
        pieces = [n.cube[i][j] for i, j in piece_indicies]
        piece_loc = [piece_map["".join(sorted(str(piece).replace(" ", ""), key=lambda c: cb.COLORS.index(c)))] for piece in pieces]
        piece_orient = [cb.ORIENT[piece.colors[0]] for piece in pieces] if piece_indicies == corner_indices else map(edge_orient, pieces)
        vector += [onehot_vector(pos, len(piece_loc)) + (onehot_vector(ori, poss)) for pos, ori in zip(piece_loc, piece_orient)]

    return "".join(map(str, cb.mat_list(vector)))

def unvectorize(vec):
    cube = cb.get_solved_cube()

    for i in range(8):
        corner_pos, corner_ori = vec[i*11:i*11+8].index('1'), vec[i*11+8:i*11+11].index('1')
        corner_str = corner_map_inverse[corner_pos]
        for j in range(corner_ori):
            corner_str = corner_str[1:] + corner_str[0]
        original_in = i in [0,3,5,6]
        new_in = corner_pos in [0,3,5,6]
        if original_in ^ new_in:
            corner_arr = list(corner_str)
            corner_arr[2], corner_arr[1] = corner_arr[1], corner_arr[2]
            corner_str = ''.join(corner_arr)
        cubie = cb.Cubie(*[cb.ORDER[cb.COLORS.index(i)] for i in corner_str])
        cube[corner_indices[i][0]][corner_indices[i][1]] = cubie

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
                cubie_arr.append(cb.ORDER[cb.COLORS.index(edge_str[temp])])
                temp += 1
        cubie = cb.Cubie(*cubie_arr)
        cube[edge_indices[i][0]][edge_indices[i][1]] = cubie

    ret = cb.Cube()
    ret.cube = cube
    return ret

if __name__ == "__main__":
    cube = cb.Cube()
    cube.turn("R F R2 U2")
    print(cube)
    vector = vectorize(cube)
    print(vector)
    cube1 = unvectorize(vector)
    print(cube1)
    print(cube.to_face())
