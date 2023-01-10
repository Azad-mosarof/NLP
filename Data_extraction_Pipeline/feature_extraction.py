import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer, TfidfVectorizer
from textblob import TextBlob
import nltk
import numpy as np
from nltk import bigrams
import itertools


text = "I am learning NLP"

#One hot encoding
# print(pd.get_dummies(text.split()))

#Count Vetorizing
text1 = ["I Love NLP and I will love learn NLP in 2months"]
vectorizer = CountVectorizer()
vectorizer.fit(text1)
vector = vectorizer.transform(text1)
# print(vectorizer.vocabulary_)
# print(vector.toarray())

#N-Gram
# print(TextBlob(text).ngrams(1))
# print(TextBlob(text).ngrams(3))

#Bigram-based features for a document
text2 = ["I will learn NLP in 2months"]
vectorizer = CountVectorizer(ngram_range=(2,2))
vectorizer.fit(text1)
vector = vectorizer.transform(text2)

# print(vectorizer.vocabulary_)
# print(vector.toarray())

#Co-occurrence Matrix
sentences = [['I', 'love', 'nlp'],
            ['I', 'love','to' 'learn'],
            ['nlp', 'is', 'future'],
            ['nlp', 'is', 'cool']]
                   
def co_occurrence_matrix(corpus):
    vocab = set(corpus)
    vocab = list(vocab)
    vocab_to_index = {word: i for i, word in enumerate(vocab)}
    bi_grams = list(bigrams(corpus))
    bigram_freq = nltk.FreqDist(bi_grams).most_common(len(bi_grams))
    co_occurrence_matrix = np.zeros((len(vocab),len(vocab)))

    for bigram in bigram_freq:
        current = bigram[0][1]
        previous = bigram[0][0]
        count = bigram[1]

        pos_current = vocab_to_index[current]
        pos_previous = vocab_to_index[previous]
        co_occurrence_matrix[pos_current][pos_previous] = count
    
    co_occurrence_matrix = np.matrix(co_occurrence_matrix)
    return co_occurrence_matrix, vocab

merged = list(itertools.chain.from_iterable(sentences))
matrix, voc = co_occurrence_matrix(merged)
coMatrixFinal = pd.DataFrame(matrix, index=voc, columns=voc)
# print(coMatrixFinal)

#Hash Vectorizing
text = ["The quick brown fox jumped over the lazy dog."]
vectorizer = HashingVectorizer(n_features=10)
vector = vectorizer.transform(text)
# print(vector.shape)
# print(vector.toarray())


#Converting text tot features using 
"""

TF-IDF: Term Frequency - Inverse Document Frquency
TF : Term frequency is simply the ratio of the count of a word present 
in a sentence, to the length of the sentence

IDF : IDF of each word is the log of
the ratio of the total number of rows to the number of rows in a particular
document in which that word is present.

IDF = log(N/n), where N is the total number of rows and n is the
number of rows in which the word was present.

TF-IDF is the simple product of TF and IDF

"""
Text = ["The quick brown fox jumped over the lazy dog.","The dog.","The fox"]
vectorizer = TfidfVectorizer()
vectorizer.fit(Text)

print(vectorizer.vocabulary_)
print(vectorizer.idf_) #In thr output “the” is appearing in all the 3 documents and it does not add much value

#Word Embeddings
"""
Word embeddings are prediction based, and they use shallow neural
networks to train the model that will lead to learning the weight and using
them as a vector representation.

word2Vec :
    There are mainly 2 types in word2vec.
    • Skip-Gram
    • Continuous Bag of Words (CBOW)

"""

sentences = [['I', 'love', 'nlp'], 
    ['I', 'will', 'learn', 'nlp', 'in', '2','months'],
    ['nlp', 'is', 'future'],
    ['nlp', 'saves', 'time', 'and', 'solves',
    'lot', 'of', 'industry', 'problems'],
    ['nlp', 'uses', 'machine', 'learning']]

import gensim
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
#training the model
# skipgram = Word2Vec(sentences, vector_size=50, window=3, min_count=1, sg=1)
# print(skipgram)





