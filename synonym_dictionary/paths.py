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

max_path_length = 20
labels = ['synonym', 'antonym']

vocab = {}
ivocab = {}

def my_intern(word):
    if not word in vocab:
        vocab[word] = len(vocab)
        ivocab[vocab[word]] = word
    return vocab[word]

edges = []
labels = []

for f in sys.argv[1:]:
    with open(f, 'r') as fd:
        for line in fd:
            fields = line.rstrip().split()
            if len(fields) >= 4:
                word1,word2,antmorph,lab = fields[0:4]
                edges.append((my_intern(word1), my_intern(word2)))
                labels.append(1+int(lab))

heads = [h for h,t in edges]
tails = [t for h,t in edges]

# print('labels range: %d - %d' % (min(labels), max(labels)), file=sys.stderr)

# vals = np.array(labels, dtype=int)+1
# print('vals range: %d - %d' % (np.min(vals), np.max(vals)), file=sys.stderr)

N = len(vocab)
G = scipy.sparse.csr_matrix((labels, (heads, tails)), shape=(N, N), dtype=np.int8)

# print('G.shape: ' + str(G.shape), file=sys.stderr)
# print('G.count_nonzero: ' + str(G.count_nonzero()), file=sys.stderr)
# print('len(labels): ' + str(len(labels)), file=sys.stderr)
# print('len(heads): ' + str(len(heads)), file=sys.stderr)
# print('len(tails): ' + str(len(tails)), file=sys.stderr)

assert len(labels) == len(heads) and len(labels) == len(tails), 'confusion pt1'

if G.count_nonzero() != len(labels):
    for h,t,l in zip(heads, tails, labels):
        if l != G[h,t]:
            print('mismatch: %d != G[%d:%s,%d:%s] = %d' % (l, h, ivocab[h], t, ivocab[t], G[h,t]), file=sys.stderr)

assert G.count_nonzero() == len(labels), 'confusion pt2'

n_comp, comp_labels = scipy.sparse.csgraph.connected_components(G, directed=False)
# print('found %d connected components' % n_comp, file=sys.stderr)

def edge(i,j):
    return max(G[i,j],G[j,i])-1

def path_to_str(path_labels):
    e = [ edge(path_labels[i-1], path_labels[i]) for i in range(1,len(path_labels))]
    n = [ ivocab[l] for l in path_labels ]
    return '\t'.join(map(str, [sum(e), len(e), '|'.join(map(str,e)), '|'.join(n)]))


memos = {}

def path(word1, word2):
    if not word1 in vocab or not word2 in vocab:
        return '-1	-1'
    iword1 = vocab[word1]
    iword2 = vocab[word2]
    if comp_labels[iword1] != comp_labels[iword2]:
        return '-1	-1'
    try: 
        if not iword1 in memos:
            memos[iword1] = scipy.sparse.csgraph.shortest_path(csgraph=G, directed=False, indices=iword1, return_predecessors=True)
    except:
        print('warning: shortest_paths failed for word: ' + word1, file=sys.stderr)
        sys.exit()
    
    dist_matrix,predecessors = memos[iword1]
    path_labels = []
    w = iword2
    while True:
        path_labels.append(w)
        d = dist_matrix[w]
        if d <= 0 or len(path_labels) >= max_path_length: 
            return path_to_str(path_labels)
        w = predecessors[w]
    # except:
    #     print('warning: shortest_paths failed for word: ' + word1, file=sys.stderr)
    #     sys.exit()
    #     return None
    # return ivocab[predecessors[iword2]] + ':' + '%d' % dist_matrix[iword2]

print('\t'.join(['word1', 'word2', 'antonym.edges', 'edges', 'labels', 'words']))

for line in sys.stdin:
    fields = line.rstrip().split()
    if len(fields) >= 2:
        word1, word2 = fields[0:2]
        print('\t'.join([line.rstrip(), str(path(word1,word2))]))
        sys.stdout.flush()
