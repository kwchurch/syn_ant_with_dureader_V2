#!/usr/bin/env python

# not finished; the problem is that labels are on edges not nodes

import numpy as np
import sys

labs={}
vocab={}
vocab_fd = open(sys.argv[1] + '.vocab', 'w')

def my_intern(word):
    if not word in vocab: 
        print(word, file=vocab_fd)
        vocab[word] = len(vocab)
    return vocab[word]

with open(sys.argv[1], 'r') as fd:
    for line in fd:
        for fields in line.rstrip().split():
            if len(fields) >= 3:
                head,tail,lab = fields
                h = my_intern(head)
                t = my_intern(tail)
                
    
