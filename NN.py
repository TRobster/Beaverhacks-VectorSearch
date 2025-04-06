import numpy as np
import json

# hey~ if you're reading this I promise there aren't any keys in this code <3

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
        context_vector = self.context_embeddings[context]
        
        # Compute dot product between target and context
        score = np.dot(target_vector, context_vector)
        probability = self.sigmoid(score)  # Sigmoid to get probability (0 to 1)
        return score, probability

    def train_step(self, target, context, label):
        score, probability = self.forward(target, context)
        
        # Compute the error (difference between predicted probability and true label)
        error = label - probability
        
        # Compute gradients for target and context embeddings
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

    # Precompute context and negative context once for each target
    for i in range(0, len(word_Context_NegContext), 3):
        target = word_Context_NegContext[i]  # Target word (encoded)
        context = findKeys(word_Context_NegContext[i + 1])  # Context words (encoded)
        neg_context = findKeys(word_Context_NegContext[i + 2])  # Negative samples

        # Efficiently append all context pairs at once
        for pos in context:
            target_words.append(target)
            context_words.append(pos)
            labels.append(1)  # Positive sample
        
        # Efficiently append all negative context pairs at once
        for neg in neg_context:
            target_words.append(target)
            context_words.append(neg)
            labels.append(0)  # Negative sample

        # Progress output to monitor
        if i % 1000 == 0:  # Print every 1000 iterations for feedback
            print(f"{i} of {len(word_Context_NegContext)}")

    # Convert lists to NumPy arrays in one step
    target_words = np.array(target_words)
    context_words = np.array(context_words)
    labels = np.array(labels)

    return target_words, context_words, labels

def findKeys(trgt):
    keysFound = []
    for trg in trgt:
        for key, value in vocab.items():
            if value == trg:
                keysFound.append(vocab[key])
    return keysFound

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

def parse_dict_string(dict_str):
    dict_str = dict_str.strip('{}')
    items = dict_str.split(', ')
    parsed_dict = {}
    for item in items:
        key, value = item.split(': ', 1)
        key = int(key)
        value = value.strip("'\"")
        parsed_dict[key] = value
    return parsed_dict

# Initialize Skip-Gram model
embedding_dim = 100
texthehe = ""
vo = ""
with open("Database/yay.txt", "r") as yay:
    yayText = (yay.read().split("\n"))
    texthehe = yayText[1]
    vo = yayText[4]
tokensCon = json.loads(texthehe)
vocablist = parse_dict_string(vo)

inverse_vocab = {i: vocablist[i] for i in range(len(vocablist))}
vocab = {index: token for token, index in inverse_vocab.items()}
print(tokensCon[:10])
for i in range(5):
    print(inverse_vocab[i])
word_Context_NegContext = tokensCon
vocab_size = len(inverse_vocab)  # Assuming vocab is the vocabulary created in getTokens()
skipgram_model = SkipGramWord2Vec(vocab_size=vocab_size, embedding_dim=embedding_dim)

# Prepare data
target_words, context_words, labels = prepare_data(word_Context_NegContext, vocab_size)

# Train the model
train(skipgram_model, target_words, context_words, labels, epochs=100, batch_size=128)

# After training, perform a vector search

query_word = vocab["decrease"]  # Query word example
similar_words = get_similar_words(query_word, skipgram_model)
print(f"Similar words to '{inverse_vocab[query_word]}':")
for i in range(len(similar_words)):
    print(inverse_vocab[similar_words[i][0]])
