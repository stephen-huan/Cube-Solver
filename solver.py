from collections import deque

import cube as cb
import representation as rep
### MORE STUFF ###

#repr_method = rep.vectorize
#repr_method = cb.fast_str
repr_method = cb.faster_rep

def solve(start, target=(cb.Cube(), cb.solved), metric=cb.HTM):
    goal, evaluate = target

    seen = [{}, {}]
    q = [deque([(start, [])]), deque([(goal, [])])]
    states = 0
    poss = 1 if goal is None else 2
    printNum = 10000

    def goal_test(node, repr, moves):
        if repr in seen[i ^ 1] if goal is not None else evaluate(node, moves):
            if goal is None: return states, moves, seen
            prefix, suffix = (moves, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], moves)
            return states, " ".join(prefix) + " " + cb.inverse(suffix), seen

    while len(q[0]) > 0 or len(q[1]) > 0:

        if len(seen[0]) > printNum:
            print(len(seen[0]))
            printNum += 10000
        
        for i in range(poss):
            n, moves = q[i].popleft()

            val = goal_test(n, repr_method(n.cube), moves)
            if val is not None: return val

            for move in metric.moves:
                if len(moves) == 0 or move[0] != moves[-1][0]:
                    states += 1
                    child = cb.Cube(n)
                    child.turn(move)
                    repr, movesp = repr_method(child.cube), moves + [move]

                    val = goal_test(child, repr, movesp)
                    if val is not None: return val

                    if repr not in seen[i]:
                        seen[i][repr] = movesp
                        q[i].append((child, movesp))

# TODO: make bidirectional
def IDdfs(start, target, metric, depth, filename):
    goal, evaluate = target

    seen = [{}, {}]
    stk = [(Cube(start), set(), [])], [(goal, set(), [])]
    states = 0
    poss = 1 if goal is None else 2

    f = open(filename, "a")

    def goal_test(node, repr, moves):
        if repr in seen[i ^ 1] if goal is not None else evaluate(node, moves):
            if goal is None: return states, moves
            prefix, suffix = (moves, seen[i ^ 1][repr]) if i == 0 else (seen[i ^ 1][repr], moves)
            return states, " ".join(prefix) + " " + cb.inverse(suffix), seen

    while len(stk[0]) > 0: #or len(stk[1]) > 0:
        for i in range(poss):
            n, path, moves = stk[i].pop()

            val = goal_test(n, repr_method(n.cube), moves)
            if val is not None: return val

            children = False
            for move in metric.moves:
                if len(moves) == 0 or move[0] != moves[-1][0]:
                    states += 1
                    child = Cube(n)
                    child.turn(move)
                    repr, movesp = repr_method(child.cube), moves + [move]

                    val = goal_test(child, repr, movesp)
                    if val is not None: return val

                    # if len(movesp) == depth:
                    #     f.write(f"{repr}: {' '.join(movesp)}\n")

                    if repr not in path and len(path) < depth:
                        children, last = True, move
                        stk[i].append((child, path | {repr}, movesp))
    f.close()

def IDsolve(start, target=(cb.Cube(), cb.solved), metric=cb.HTM, maxdepth=float("INF"), filename="temp.pickle"):
    rtn, depth = None, 0
    while rtn is None and depth <= maxdepth:
        rtn = IDdfs(start, target, metric, depth, filename)
        print(depth)
        depth += 1
    return rtn

if __name__ == "__main__":
#    repr_method = cb.fast_str
#    cube = import_cube("test.txt")
    cube = cb.Cube()
    cube.turn("R U R'")
    print(cube)
    states, alg, seen = solve(cube, (cb.Cube(), cb.solved), cb.HTM)
    print(states, alg, len(cb.tokenize(alg)))
