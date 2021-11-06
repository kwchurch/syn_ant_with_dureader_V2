#!/usr/bin/env python

import numpy as np
from numpy import linalg
import annoy,gensim,sys,os,argparse,scipy,pdb

import sklearn
from sklearn.preprocessing import normalize

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import editdistance

labels = ['synonym', 'antonym']

def load_triples(file, labels):
    res = []
    with open(file, 'r') as fd:
        for line in fd:
            fields = line.rstrip().split()
            h,r,t = fields[0:3]
            print('\t'.join(['triples', labels[h], h, r, labels[t], t, file]))
            res.append([labels[h], r, labels[t]])
    return res

vocab = {}
ivocab = {}

def my_intern(word):
    if not word in vocab:
        vocab[word] = len(vocab)
        ivocab[vocab[word]] = word
    return vocab[word]

pairs_of_pairs = [[], []]

for line in sys.stdin:
    fields = line.rstrip().split()
    if len(fields) >= 3:
        word1,word2,lab = fields[0:3]
    pairs_of_pairs[int(lab)].append((my_intern(word1), my_intern(word2)))


heads = [h for h,t in pairs_of_pairs[0]]
tails = [t for h,t in pairs_of_pairs[0]]
N = len(vocab)
G = scipy.sparse.csr_matrix((np.ones(len(heads), dtype=np.int8), (heads, tails)), shape=(N, N), dtype=bool)
n_comp, comp_labels = scipy.sparse.csgraph.connected_components(G, directed=False)

for w,lab in enumerate(comp_labels):
    print(str(lab) + '\t' + ivocab[w])
