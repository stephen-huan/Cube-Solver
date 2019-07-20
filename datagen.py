from cube import *
from collections import deque
import numpy as np

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
    data = small_datagen(2)
    save_data('training_data.csv', data)