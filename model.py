from tensorflow.keras.models import load_model
import numpy as np
import torch 
from torch import nn

class tensorflow_predictor:
    def __init__(self):
        self.model = load_model('MNIST_CNN_model.h5')

    def __call__(self, x):
        if x.shape[0] != 28:
            x = resize(x, (28,28))
        x = x.reshape(1,28,28,1)
        result = np.argmax(self.model.predict(x, verbose = 0))
        return result

class torch_predictor:
    def __init__(self):
        self.model = nn.Linear(784, 10)

    def __call__(self, x):
        input_tensor = torch.Tensor(x)
        input_tensor = input_tensor.reshape(1, 784)
        result = np.argmax(self.model(input_tensor).detach().numpy())
        return result