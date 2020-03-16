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

corner_lookup = {}
for key in corner_map:
    corner_lookup[key] = key
    arr = [*key]
    perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
    for a,b,c in perms:
        arr = [arr[a],arr[b],arr[c]]
        corner_lookup[''.join(arr)] = key
        arr = [*key]

corner_map_inverse = cb.inv(corner_map)
corner_indices = [(0, 0), (0, 2), (0, 6), (0, 8), (2, 0), (2, 2), (2, 6), (2, 8)]

edge_map = {
    'WB ': 0,
    'WO ': 1,
    'WR ': 2,
    'WG ': 3,
    'BO ': 4,
    'BR ': 5,
    'GO ': 6,
    'GR ': 7,
    'YB ': 8,
    'YO ': 9,
    'YR ': 10,
    'YG ': 11,
}

edge_lookup = {}
for key in edge_map:
    edge_lookup[key] = key
    arr = [*key]
    perms = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]
    for a,b,c in perms:
        arr = [arr[a],arr[b],arr[c]]
        edge_lookup[''.join(arr)] = key
        arr = [*key]

edge_correct_ori = set([i.replace(" ","") for i in edge_map])
edge_map_inverse = cb.inv(edge_map)
edge_indices = [(0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,6), (1,8), (2,1), (2,3), (2,5), (2,7)]
edge_gap_positions = [2, 1, 1, 2, 0, 0, 0, 0, 2, 1, 1, 2]

def edgeOrient(edge):
    edge = str(edge).replace(" ", "")
    return int(cb.COLORS.index(edge[0]) > cb.COLORS.index(edge[1]))

def bits_to_string(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def onehot_vector(index, length):
    l = [0]*length
    l[index] = 1
    return l

def vectorize(cube, compress = False):
    corner_loc, corner_orient, edge_loc, edge_orient = [],[],[],[]
    corners = [cube[i][j] for i,j in corner_indices]
    for corner in corners:
        temp = corner_map[corner_lookup[str(corner)]]
        corner_loc.append(str(temp))
        corner_orient.append(str(cb.ORIENT[corner.colors[0]]))

    edges = [cube[i][j] for i,j in edge_indices]
    for edge in edges:
        temp = edge_map[edge_lookup[str(edge)]]
        edge_loc.append(str(temp))
        edge_orient.append(str(0 if str(edge).replace(" ", "") in edge_correct_ori else 1))
    
    vector = []
    if compress:
        vector.append(';'.join(corner_loc))
        vector.append(int(''.join(corner_orient),3)) #Convert this to a decimal number so it takes up less space, basically do ternary -> decimal
        vector.append(';'.join(edge_loc))
        vector.append(int(''.join(edge_orient),2)) #Same as corner_orient, except binary

#    else:
#        vector += [(pos, len(piece_loc)) + (ori, poss) for pos,ori in zip(piece_loc, piece_orient)]
#        vector += [onehot_vector(pos, len(piece_loc)) + (onehot_vector(ori, poss)) for pos, ori in zip(piece_loc, piece_orient)]

    return vector

def unvectorize(vec, compressed = False):
    cube = cb.get_solved_cube()
    if compressed:
        split = vec.strip().split(" ")
        corner_posses = split[0].split(";")
        corner_oris = str(np.base_repr(int(split[1]), 3))
        corner_oris = "0"*(8 - len(corner_oris)) + corner_oris
        edge_posses = split[2].split(";")
        edge_oris = str(np.base_repr(int(split[3]), 2))
        edge_oris = "0"*(12 - len(edge_oris)) + edge_oris

    for i in range(8):
        if compressed:
            corner_pos, corner_ori = int(corner_posses[i]), int(corner_oris[i])
        else:
            corner_pos, corner_ori = vec[i*11:i*11+8].index('1'), vec[i*11+8:i*11+11].index('1')
        corner_str = corner_map_inverse[corner_pos]
        for j in range(corner_ori):
            corner_str = corner_str[1:] + corner_str[0]
        original_in = i in [0,3,5,6]
        new_in = corner_pos in [0,3,5,6]
        if original_in ^ new_in == True:
            corner_arr = list(corner_str)
            corner_arr[2], corner_arr[1] = corner_arr[1], corner_arr[2]
            corner_str = ''.join(corner_arr)
        cubie = cb.Cubie(*[cb.ORDER[cb.COLORS.index(i)] for i in corner_str])
        cube[corner_indices[i][0]][corner_indices[i][1]] = cubie

    for i in range(12):
        if compressed:
            edge_pos, edge_ori = int(edge_posses[i]), int(edge_oris[i])
        else:
            edge_pos, edge_ori = vec[i*14+88:i*14+100].index('1'), vec[i*14+100:i*14+102].index('1')
        edge_str = edge_map_inverse[edge_pos]
        if edge_ori == 1:
            edge_str = edge_str[::-1]
            if edge_str[0] == " ":
                edge_str = edge_str[1:] + " "
            elif edge_str[-1] == " ":
                edge_str = " " + edge_str[1:]
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

def speedtest():
    from time import time
    start = time()
    cube = cb.Cube()
    for i in range(10000):
        cube.turn("R")
        vector = vectorize(cube.cube)
    print(time()-start)

if __name__ == "__main__":
    file = open("data/removed/removed_1.txt","r")
    lines = file.readlines()
    file.close()
    import random
    for i in range(100000):
        cub = cb.Cube()
        for j in range(15):
            thing = random.choice(["R", "R2", "R'", "L", "L2", "L'", "B", "B2", "B'", "U", "U2", "U'", "F", "F2", "F'", "D", "D2", "D'"])
            cub.turn(thing)
        if str(unvectorize(' '.join([str(i) for i in vectorize(cub.cube, True)]), True)) == str(cub) == False:
            print(cub.cube)
#        print(vectorize(cub.cube, True))
#        print(unvectorize(' '.join([str(i) for i in vectorize(cub.cube, True)]), True))
#        print()
#    speedtest()

    
#    cube1 = unvectorize(vector)
#    print(cube1)
#    print(cube.to_face())
