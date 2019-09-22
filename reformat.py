"""
Used to reformat data that we downloaded.
Will be different for each datafile based on its format.
"""

import cube as cb
import representation as repr
from time import time
from multiprocessing import Process, freeze_support

NUM_PROCESSES = 2

def add(moves, files):
    cube = cb.Cube()
    cube.turn(' '.join(moves))
    length = len(moves)
    for i in range(length):
        fast = cb.fast_str(cube.cube)
        vector = repr.vectorize(cube.cube)
        vector = [str(i) for i in vector]
        files[length-i].write(''.join(vector))
        cube.turn(cb.opposite(moves[-i-1]))

def htm(filename="raw_data/htm.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        each = len(lines) // NUM_PROCESSES
        for pnum in range(NUM_PROCESSES):
            process = Process(target=process_htm, args=(lines[pnum*each:(pnum+1)*each],pnum))
            process.daemon = True
            process.start()
        x = input()            

def process_htm(lines, pnum):
    filename = "data/reformatted%s_%s.txt"
    start = time()
    files = []
    for i in range(21):
        file = open(filename % (i,pnum), "a+")
        files.append(file)
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
        add(moves, files)
        if index > checkpoint:
            print(checkpoint)
            print(time() - start)
            start = time()
            checkpoint += 1000
        index += 1
    for file in files:
        file.close()

def _100k(filename="raw_data/100000optcubes.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(len(lines))
        checkpoint = 0
        index = 0
        for line in lines:
            line = line.strip()
            moves = line[:line.index("(")-1].strip().split(" ")
            if index > checkpoint:
                print(checkpoint)
                checkpoint += 1000
            index += 1

def save(seqs):
    global SAVED
    output = ""
    for vector, distance in seqs:
        output += vector + ";" + str(distance) + "\n"
    file.write(output)
    SAVED += len(seqs)
    
if __name__ == "__main__":
    freeze_support()
    htm()
#_100k()
#seqs = set()
#save(filename="reformatted.txt")