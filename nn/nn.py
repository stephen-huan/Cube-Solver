from keras import Sequential, Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.models import model_from_json
import cube as cb
import heapq

class Node:

    def __init__(self, state, depth, parent):
        self.state = state
        self.depth = depth
        self.parent = parent
        self.moves = []
    
    def get_neighbors(self):
        neighbors = []
        for move in self.moves:
            neighbor = cb.Cube(self.state, init_cube=True)
            neighbor.turn(move)
            neighbors.append(Node(neighbor, self.depth + 1, parent=self))

    def setF(self, f):
        self.f = f

    def __lt__(self, other):
      return self.depth + self.f < other.depth + other.f

    def __eq__(self, other):
        return other.depth + other.f == self.depth + self.f


class NN:
    
    def __init__(self, input_shape, output_shape, lr):
        
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = self.build_model(lr)
    
    def __init__(self, model):
        self.model = model
    
    def build_model(self, lr):
        
        model = Sequential()
        # Convolutions.
        model.add(Dense(256, activation='relu', input_shape=self.input_shape))
        model.add(Dropout(0.5))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.output_shape, activation='softmax'))
        sgd = SGD(lr=lr, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        model.summary()
        self.model = model

    def train(X, y, epochs, batch_size):
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size)

    def evaluate(X_test, y_test):
        return self.model.evaluate(X_test, y_test, batch_size=128)
    
    def predict(X):
        return self.model.predict(X)
    
    def save(filepath):
        with open(filepath + '.json', 'w') as f:
            f.write(self.model.to_json())
        self.model.save_weights(filepath + '.h5')
    
    def solve(start, goal = cb.Cube()):
        #TODO: Add calculation of heuristic to node
        openSet = [Node(start, 1, None)]
        closedSet = set()
        while len(openSet) > 0:
            node = heapq.heappop(openSet)
            if node.state.fast_str() in closedSet:
                continue
            closedSet.add(node.state)
            if node.state.fast_str() == goal.fast_str():
                print("Solved: ", node.depth)
                break
            for nbr in node.get_neighbors():
                if nbr not in closedSet:
                    heapq.heappush(openSet, nbr)

def load_model(filepath):
    with open(filepath + '.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights(filepath + '.h5')
    nn = NN(model)
