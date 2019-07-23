from keras import Sequential, Dense, Dropout, Activation
from keras.optimizers import SGD

class NN:
    
    def __init__(self, input_shape, output_shape, model, lr):
        
        self.input_shape = input_shape
        self.output_shape = output_shape
        if model:
            self.model = model
        else:
            self.model = self.build_model(lr)
    
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
