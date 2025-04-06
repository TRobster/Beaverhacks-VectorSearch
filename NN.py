import numpy as np
import random
from Vectonizer import getTokens

class SkipGramWord2Vec:
    def __init__(self, vocab_size, embedding_dim, learning_rate=0.1):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        
        # Randomly initialize target and context embeddings (weight matrices)
        self.target_embeddings = np.random.randn(vocab_size, embedding_dim)
        self.context_embeddings = np.random.randn(vocab_size, embedding_dim)
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def forward(self, target, context):
        target_vector = self.target_embeddings[target]
        while context >= vocab_size:
            context -= vocab_size
        context_vector = self.context_embeddings[context]
        # print(inverse_vocab[context])
        # print(inverse_vocab[target[0]])
        
        # Compute dot product between target and context
        score = np.dot(target_vector, context_vector)
        probability = self.sigmoid(score)  # Sigmoid to get probability (0 to 1)
        return score, probability

    def train_step(self, target, context, label):
        score, probability = self.forward(target, context)
        
        # Compute the error (difference between predicted probability and true label)
        error = label - probability
        
        # Compute gradients for target and context embeddings
        while context >= vocab_size:
            context -= vocab_size
        target_gradient = error * self.context_embeddings[context]
        context_gradient = error * self.target_embeddings[target]

        # Ensure context_gradient is a 1D array of shape (embedding_dim,)
        context_gradient = context_gradient.reshape(self.embedding_dim)
        
        # Update embeddings using gradient descent
        self.target_embeddings[target] += self.learning_rate * target_gradient
        self.context_embeddings[context] += self.learning_rate * context_gradient
        
        return error, probability
    
def prepare_data(word_Context_NegContext, vocab_size):
    target_words = []
    context_words = []
    labels = []
    
    for i in range(len(word_Context_NegContext)):

        if not i%3 == 0:
            continue
        target = word_Context_NegContext[i]  # Target word (encoded)
        context = word_Context_NegContext[i+1]  # Context word (encoded)
        neg_context = word_Context_NegContext[i+2]  # Negative samples
        
        # Positive context pairs
        target_words.append(target)
        for pos in context:
            context_words.append(pos)
        labels.append(1)  # Positive sample
        
        # Negative context pairs
        for neg in neg_context:
            target_words.append(target)
            context_words.append(neg)
            labels.append(0)  # Negative sample

    return np.array(target_words), np.array(context_words), np.array(labels)

def train(skipgram_model, target_words, context_words, labels, epochs=10, batch_size=64):
    num_samples = len(target_words)
    
    for epoch in range(epochs):
        total_loss = 0
        
        # Randomly shuffle the data at the start of each epoch
        indices = np.random.permutation(num_samples)
        target_words = target_words[indices]
        context_words = context_words[indices]
        labels = labels[indices]
        
        for i in range(0, num_samples, batch_size):
            # Get the batch data
            batch_targets = target_words[i:i + batch_size]
            batch_contexts = context_words[i:i + batch_size]
            batch_labels = labels[i:i + batch_size]

            # print("batch targs: ",batch_targets)
            # print("batch contex: ",batch_contexts)
            # print("batch lab: ",batch_labels)
            
            batch_loss = 0
            for target, context, label in zip(batch_targets, batch_contexts, batch_labels):
                error, _ = skipgram_model.train_step(target, context, label)
                batch_loss += error**2  # Squared error as part of loss
            
            total_loss += batch_loss / batch_size
        
        print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss / num_samples}")

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def get_similar_words(word, skipgram_model, top_n=5):
    word_vector = skipgram_model.target_embeddings[word]
    similarities = []
    
    for i in range(skipgram_model.vocab_size):
        if i != word:  # Don't compare the word with itself
            sim = cosine_similarity(word_vector, skipgram_model.target_embeddings[i])
            similarities.append((i, sim))
    
    # Sort by similarity in descending order and get the top N words
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_n]
    
    return [(i, sim) for i, sim in similarities]

# Initialize Skip-Gram model
embedding_dim = 100
word_Context_NegContext, inverse_vocab = getTokens()
vocab_size = len(inverse_vocab)  # Assuming vocab is the vocabulary created in getTokens()
skipgram_model = SkipGramWord2Vec(vocab_size=vocab_size, embedding_dim=embedding_dim)

# Prepare data
target_words, context_words, labels = prepare_data(word_Context_NegContext, vocab_size)

# Train the model
train(skipgram_model, target_words, context_words, labels, epochs=100, batch_size=128)

# After training, perform a vector search
vocab = {index: token for token, index in inverse_vocab.items()}
query_word = vocab["decrease"]  # Query word example
similar_words = get_similar_words(query_word, skipgram_model)
print(f"Similar words to '{inverse_vocab[query_word]}':")
for i in range(len(similar_words)):
    print(inverse_vocab[similar_words[i][0]])