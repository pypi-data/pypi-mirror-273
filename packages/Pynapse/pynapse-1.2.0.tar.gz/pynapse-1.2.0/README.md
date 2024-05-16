# VERSION

*MAJOR.MINOR.PATCH*

# USAGE EXAMPLES

### VIDEO TUTORIAL

https://www.youtube.com/watch?v=arrJuppqFPE

### EXAMPLE FOR SAVING (remove Net_Save to not save your network)

```python
from Pynapse import Dense, Activation_Sigmoid, Network, Net_Save, Activation_ReLU, Bin_Round
import numpy as np

layers = [
    Dense(2, 10),             # 2 inputs, 10 output connections
    Activation_ReLU(),        # ReLU activation function
    Dense(10, 1),             # 10 inputs (output from previous layer), 1 output neuron
    Activation_Sigmoid()      # Sigmoid activation function for output to be between 1 and 0
]


net = Network(layers)                               # Set the network to use the provided layers

X = np.array([[0,0], [0,1], [1,0], [1,1]])          # Training data for a simple OR function
y = np.array([[0],[1],[1],[1]])                     # Results to aim for

net.train(X, y, epochs=200, lr=0.1)                 # Train the network with the provided data

Net_Save.save('model.json', layers)                 # Save the network to a json file

print(net.forward(np.array([[1,0]])))               # Putting data through the network, result should be near one based off the data    e.g. [[0.91807402]]
print(net.forward(np.array([[1,0]]))[0][0])         # You can remove brackets like this     e.g. 0.9180740216494526

prediction = net.forward(np.array([[1,0]]))[0][0]   # You can remove brackets in a variable like this
print(prediction)

prediction = Bin_Round.Bin_Round(net.forward(np.array([[1,0]])))
print(prediction)                                   # Round the output of the output of the output layer to binary 1 or 0    e.g. 1
```


### EXAMPLE FOR LOADING

```python
from Pynapse import Dense, Activation_Sigmoid, Network, Net_Save, Activation_ReLU
import numpy as np

layers = [
    Dense(2, 10),             # 2 inputs, 10 output connections
    Activation_ReLU(),        # ReLU activation function
    Dense(10, 1),             # 10 inputs (output from previous layer), 1 output neuron
    Activation_Sigmoid()      # Sigmoid activation function for output to be between 1 and 0
]


net = Network(layers)                               # Set the network to use the provided layers

Net_Save.load('model.json', layers)                 # Load the network from a json file

prediction = net.forward(np.array([[1,0]]))[0][0]   # You can remove brackets in a variable like this
print(prediction)                                   # Print the prediction
```

# CHANGES
- changed printing output loss from (output - y) to cross entropy


# WHY NAMED "Pynapse"
#### This module has been named "Pynapse" meaning Python and Synapse