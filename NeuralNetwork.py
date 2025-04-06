"""
Author: Trevor Robbins (Back-end)
Date: 4/5/2025
Origin: Beaverhacks Hackathon
Purpose: Create neural network "backbone" for vector search algorithm 
"""

import Vectonizer as vector
import numpy as np

# Activation function and derivative
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Tokenize the data
word_Context_NegContext, inverse_vocab = vector.getTokens()

print(type(inverse_vocab))
print(inverse_vocab[0])

# Prepare the input data for the neural network
X = []
y = []
words_used = []

for i in range(int(len(word_Context_NegContext)/3.0)):
    if not words_used.__contains__(word_Context_NegContext[i][0]):
        words_used.append(word_Context_NegContext[i][0])
        word = inverse_vocab[word_Context_NegContext[i][0]]
    context_words = word_Context_NegContext[i+1]
    negative_context_words = word_Context_NegContext[i+2]

    for context_word in context_words:
        X.append([word, context_word])
        y.append(1)  # Positive context

    for neg_context_word in negative_context_words:
        X.append([word, neg_context_word])
        y.append(0)  # Negative context

# Weights
np.random.seed(42)
embedding_dim = 50  # Dimension of the word embeddings
W1 = np.random.randn(len(vocab), embedding_dim)
W2 = np.random.randn(embedding_dim, len(vocab))

# Training loop
lr = 0.1

class Trainer:
    def __init__(self, X, y, W1, lr):
        self.X = X
        self.y = y
        self.W1 = W1
        self.lr = lr

    def train(self, epochs):
        for epoch in range(epochs):
            # Forward pass
            z1 = self.W1[self.X[:, 0]]  # Embedding for the target word
            z2 = self.W1[self.X[:, 1]]  # Embedding for the context/negative word
            dot_product = np.sum(z1 * z2, axis=1, keepdims=True)
            y_pred = sigmoid(dot_product)

            # Loss (Binary Cross-Entropy)
            loss = -np.mean(self.y * np.log(y_pred) + (1 - self.y) * np.log(1 - y_pred))

            # Backpropagation
            dloss = y_pred - self.y.reshape(-1, 1)
            dW1_target = dloss * z2
            dW1_context = dloss * z1

            # Update weights
            for i in range(len(self.X)):
                self.W1[self.X[i, 0]] -= self.lr * dW1_target[i]
                self.W1[self.X[i, 1]] -= self.lr * dW1_context[i]

            if epoch % 1000 == 0:
                print(f"Epoch {epoch} | Loss: {loss:.4f}")

# Instantiate and train the model
trainer = Trainer(X, y, W1, W2, lr)
trainer.train(10000)


from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Load the word embeddings
word_embeddings = W1
vocab = {v: k for k, v in vocab.items()}  # Inverse vocab to get words from indices

# Function to find the most similar words
def find_similar_words(word, top_n=5):
    word_idx = vocab[word]
    word_vec = word_embeddings[word_idx].reshape(1, -1)
    similarities = cosine_similarity(word_vec, word_embeddings)[0]
    similar_indices = similarities.argsort()[-top_n-1:-1][::-1]
    similar_words = [vocab[idx] for idx in similar_indices]
    return similar_words

# Example: Find similar words to "king"
similar_words = find_similar_words("king")
print(f"Words similar to 'king': {similar_words}")

# Function to solve word analogies
def word_analogy(word1, word2, word3):
    vec1 = word_embeddings[vocab[word1]]
    vec2 = word_embeddings[vocab[word2]]
    vec3 = word_embeddings[vocab[word3]]
    analogy_vec = vec1 - vec2 + vec3
    similarities = cosine_similarity(analogy_vec.reshape(1, -1), word_embeddings)[0]
    best_match = similarities.argsort()[-2]  # Exclude the input word itself
    return vocab[best_match]

# Example: Solve analogy "king - man + woman = ?"
analogy_result = word_analogy("king", "man", "woman")
print(f"'king' - 'man' + 'woman' = '{analogy_result}'")

# Visualize embeddings using t-SNE
def visualize_embeddings(words):
    word_indices = [vocab[word] for word in words]
    word_vectors = word_embeddings[word_indices]
    tsne = TSNE(n_components=2)
    reduced_vectors = tsne.fit_transform(word_vectors)
    plt.figure(figsize=(10, 10))
    for i, word in enumerate(words):
        plt.scatter(reduced_vectors[i, 0], reduced_vectors[i, 1])
        plt.annotate(word, (reduced_vectors[i, 0], reduced_vectors[i, 1]))
    plt.show()

# Example: Visualize embeddings for a set of words
words_to_visualize = ["king", "queen", "man", "woman", "dog", "cat", "lion"]
visualize_embeddings(words_to_visualize)