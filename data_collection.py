import os

def merge_multiprocess(pattern, procs, length, output):
    files = os.listdir("data/")
    for i in range(1, length):
        out = open(output % i, "w+")
        for j in range(procs):
            file = open(pattern % (i,j), "r")
            lines = file.read().strip()
            out.write(lines+"\n")
            file.close()
        out.close()
        print(i)

def remove_duplicates(pattern, length, new_pattern):
    for i in range(1, length):
        file = open(pattern % i, "r")
        lines = file.readlines()
        lines = [i.strip() for i in lines]
        distinct = set(lines)
        print(len(lines), len(distinct))
        file_removed = open(new_pattern % i, "w+")
        file_removed.write('\n'.join(distinct))

if __name__ == '__main__':
#    merge_multiprocess("data/merged/reformatted%s_%s.txt", 16, 21, "data/merged/merged_%s.txt")
    remove_duplicates('data/merged/merged_%s.txt', 21, 'data/removed/removed_%s.txt')
