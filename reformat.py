"""
Used to reformat data that we downloaded.
Will be different for each datafile based on its format.
"""

import cube as cb
import representation as repr
from time import time

global SAVED
SAVED = 0
SAVE_POINT = 10000
filename = "reformatted.txt"
file = open(filename, "a+")
seqs = set()

def add(seqs, moves):
    cube = cb.Cube()
    cube.turn(' '.join(moves))
    length = len(moves)
    for i in range(length):
#        vector = repr.vectorize(cube.cube)
#        seqs.add((''.join([''.join(list(map(str, i))) for i in vector]), length-i))
#        cube.turn(cb.opposite(moves[-i-1]))
        pass
    if len(seqs) > SAVE_POINT:
        save(seqs)
        seqs = set()

def htm(seqs, filename="data/htm.txt"):
    with open(filename, 'r') as file:
        start = time()
        lines = file.readlines()
        print(len(lines))
        checkpoint = 0
        index = 0
        for line in lines:
            line = line.strip()
            length = int(len(line) / 2) #Should be 20 for all of them but not sure
            moves = []
            for i in range(length):
                move = line[i*2:i*2+2]
                if move[-1] == "3":
                    move = move[0] + "'"
                elif move[-1] == "1":
                    move = move[0]
                moves.append(move)
#            process = Process(target=add, args=(moves,))
#            process.start()
            add(seqs, moves)
            if index > checkpoint:
                print(checkpoint)
                print(time() - start)
                start = time()
                checkpoint += 10000
            index += 1

def _100k(seqs, filename="data/100000optcubes.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(len(lines))
        checkpoint = 0
        for line in lines:
            line = line.strip()
            moves = line[:line.index("(")-1].strip().split(" ")
            add(seqs, moves)
            if SAVED > checkpoint:
                print(checkpoint)
                checkpoint += 10000

def save(seqs):
    global SAVED
    for vector, distance in seqs:
        file.write(vector + " " + str(distance) + "\n")
    SAVED += len(seqs)
    
htm(seqs)
_100k(seqs)
save(seqs)
seqs = set()
file.close()
#save(filename="reformatted.txt")