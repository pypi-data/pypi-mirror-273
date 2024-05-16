import numpy as np
import json

class Dense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = np.random.randn(n_inputs, n_neurons) #* .1# * np.sqrt(2 / n_inputs) * .3#  * (.8  * n_inputs)
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases

    def backward(self, dvalues):
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = np.dot(dvalues, self.weights.T)


class Activation_Sigmoid:
    def forward(self, x):
        self.output = 1 / (1 + np.exp(-x))

class Activation_ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)
    
class Network:
    def __init__(self, layers):
        self.layers = layers
    
    def forward(self, X):
        for layer in self.layers:
            layer.forward(X)
            X = layer.output
        return X

    def backward(self, dvalues):
        for layer in reversed(self.layers):
            if isinstance(layer, Activation_Sigmoid):
                dvalues *= layer.output * (1 - layer.output)  # Sigmoid derivative
            if hasattr(layer, 'backward'):
                layer.backward(dvalues)
                dvalues = layer.dinputs


    def train(self, X, y, epochs, lr=0.1, v=True):
        if v == True: # made like this so we are not checking if v = true to print many times (to hopefully be faster than constantly checking)
            for epoch in range(epochs):
                output = self.forward(X)
                loss = self.cross_entropy(y, output)
                self.backward(output - y)

                #update weights and biases
                for layer in self.layers:
                    if hasattr(layer, 'weights'):
                        layer.weights -= lr * layer.dweights
                        layer.biases -= lr * layer.dbiases
                print(f"Epoch: {epoch} Loss: {loss}")
        else:
            for epoch in range(epochs):
                output = self.forward(X)
                loss = self.cross_entropy(y, output)
                self.backward(output - y)

                #update weights and biases
                for layer in self.layers:
                    if hasattr(layer, 'weights'):
                        layer.weights -= lr * layer.dweights
                        layer.biases -= lr * layer.dbiases

    def cross_entropy(self, y_true, y_pred):
        # Avoid numerical instability by adding a small epsilon
        epsilon = 1e-15
        y_pred_clipped = np.clip(y_pred, epsilon, 1 - epsilon)
        # Compute cross-entropy loss
        return -np.mean(y_true * np.log(y_pred_clipped) + (1 - y_true) * np.log(1 - y_pred_clipped))

class Bin_Round:
    def Bin_Round(X):
        if X >= 0.5:
            return 1
        elif X < 0.5:
            return 0
        else:
            return 2

class Net_Save:
    def save(file_name, dense_list):
        data = {}
        for i, dense in enumerate(dense_list):
            if hasattr(dense, 'weights'):
                data[f'dense_{i}_weights'] = dense.weights.tolist()
                data[f'dense_{i}_biases'] = dense.biases.tolist()
        data = json.dumps(data, indent=2)
        with open(file_name, 'w') as f:
            f.write(data)
    
    def load(file_name, dense_list):
        with open(file_name, 'r') as f:
            data = json.load(f)

        for i, dense in enumerate(dense_list):
            if hasattr(dense, 'weights'):
                dense.weights = np.array(data[f'dense_{i}_weights'])
                dense.biases = np.array(data[f'dense_{i}_biases'])