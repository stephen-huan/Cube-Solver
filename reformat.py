"""
Used to reformat data that we downloaded.
Will be different for each datafile based on its format.
"""

import cube as cb
import representation as repr
from multiprocessing import Process
seqs = set()

def add(moves):
    cube = cb.Cube()
    cube.turn(' '.join(moves))
    length = len(moves)
    for i in range(length):
        vector = repr.vectorize(cube.cube)
        seqs.add((''.join([''.join(list(map(str, i))) for i in vector]), length-i))
        cube.turn(cb.opposite(moves[-i-1]))

def htm(filename="data/htm.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(len(lines))
        checkpoint = 0
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
            process = Process(target=add, args=(moves,))
            process.start()
            add(moves)
            if len(seqs) > checkpoint:
                print(checkpoint)
                checkpoint += 10000

def _100k(filename="data/100000optcubes.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(len(lines))
        checkpoint = 0
        for line in lines:
            line = line.strip()
            moves = line[:line.index("(")-1].strip().split(" ")
            add(moves)
            if len(seqs) > checkpoint:
                print(checkpoint)
                checkpoint += 10000

def save(filename):
    with open(filename, "a+") as file:
        for vector, distance in seqs:
            file.write(vector + " " + str(distance) + "\n")
        file.close()
htm()
_100k()

save(filename="reformatted.txt")