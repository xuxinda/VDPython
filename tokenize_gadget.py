import sys
import pandas
from gensim.models import Word2Vec
import numpy

# DEBUG
#import joblib
#import pprint
#df = joblib.load('df.dump')
# ##

# Sets for operators
operators3 = {'<<=', '>>='}
operators2 = {
    '->', '++', '--', 
    '!~', '<<', '>>', '<=', '>=', 
    '==', '!=', '&&', '||', '+=', 
    '-=', '*=', '/=', '%=', '&=', '^=', '|='
    }
operators1 = { 
    '(', ')', '[', ']', '.', 
    '+', '-', '*', '&', '/', 
    '%', '<', '>', '^', '|', 
    '=', ',', '?', ':' , ';',
    '{', '}'
    }

# Input: string 
def tokenize(line):
    tmp, w = [], []
    i = 0
    while i < len(line):
        # Ignore spaces and combine previously collected chars to form words
        if line[i] == ' ':
            tmp.append(''.join(w))
            tmp.append(line[i])
            w = []
            i += 1
        # Check operators and append to final list
        elif line[i:i+3] in operators3:
            tmp.append(''.join(w))
            tmp.append(line[i:i+3])
            w = []
            i += 3
        elif line[i:i+2] in operators2:
            tmp.append(''.join(w))
            tmp.append(line[i:i+2])
            w = []
            i += 2
        elif line[i] in operators1:
            tmp.append(''.join(w))
            tmp.append(line[i])
            w = []
            i += 1
        # Character appended to word list
        else:
            w.append(line[i])
            i += 1
    # Filter out irrelevant strings
    res = list(filter(lambda c: c != '', tmp))
    return list(filter(lambda c: c != ' ', res))

def vectorize(gadget):
    tokenized = []
    for line in gadget:
        tokenized.append(tokenize(line))
    model = Word2Vec(tokenized, min_count=1)
    embeddings = model.wv
    del model
    vectors = []
    size = 0
    for line in tokenized:
        for token in line:
            size += 1
            embedding = embeddings[token]
            if vectors == []:
                vectors = embedding
            else:
                vectors = numpy.add(vectors, embedding)
    return numpy.true_divide(vectors, size)
    

# Input: dataframe
def tokenize_df(df):
    tokenized_gadgets = []
    # Apply tokenize to every line of dataframe
    for line in range(len(df['gadget'])):
        l = list(map(tokenize, df["gadget"][line]))
        tokenized_gadgets.append(l)
    df['tokenized_gadget'] = tokenized_gadgets
    return df

# Debug
# df = tokenize_df(df)
# print(len(df['tokenized_gadget'][0]))
# print(len(df['gadget'][0]))
#  ##