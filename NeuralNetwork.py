"""
Author: Trevor Robbins (Back-end)
Date: 4/5/2025
Origin: Beaverhacks Hackathon
Purpose: Create neural network "backbone" for vector search algorithm 
"""

import os, sys
import numpy as np


# Activation function and derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # XOR input
y = np.array([[0], [1], [1], [0]])             # XOR output

# Weights
np.random.seed(42)
W1 = np.random.randn(2, 3)
b1 = np.zeros((1, 3))
W2 = np.random.randn(3, 1)
b2 = np.zeros((1, 1))

# Training loop
lr = 0.1
class Trainer():
    for epoch in range(10000):
        # Forward pass
        z1 = X @ W1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ W2 + b2
        y_pred = sigmoid(z2)

        # Loss (MSE)
        loss = np.mean((y - y_pred) ** 2)

        # Backpropagation
        dloss = 2 * (y_pred - y)
        dz2 = dloss * sigmoid_deriv(z2)
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        dz1 = dz2 @ W2.T * sigmoid_deriv(z1)
        dW1 = X.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        # Update weights
        W2 -= lr * dW2
        b2 -= lr * db2
        W1 -= lr * dW1
        b1 -= lr * db1

        if epoch % 1000 == 0:
            print(f"Epoch {epoch} | Loss: {loss:.4f}")



