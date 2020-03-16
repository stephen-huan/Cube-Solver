from collections import deque
import cube
import linear as lin

def fast_str(m): return  "".join(map(str, cube.mat_list(m)))

def solved(cube, *args): return fast_str(cube.cube) == fast_str(cube.get_solved_cube())

def group(seq):
    temp = cube.StickerCube()
    temp.turn(seq)
    i = 0
    while not solved(temp):
        temp.turn(seq)
        i += 1
    return i + 1

def bfs(n):
    q = deque([("", "", 0)])
    d = {}
    while len(q) > 0:
        seq, last, l = q.pop()
        d[seq] = group(seq)
        if l < n:
            for move in cube.MOVES:
                if move != last:
                    q.append((seq + " " + move, move, l + 1))
                    q.append((seq + " " + move + "'", move, l + 1))
                    q.append((seq + " " + move + "2", move, l + 1))
    return d

# print(sorted(bfs(5).items(), key=lambda x: (-x[1], x[0]))[:10000])
# print(group("R U2 D' B D'"))
