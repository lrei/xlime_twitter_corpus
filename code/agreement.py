#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
agreement.py
Calculates agreement measures
adapted from
https://en.wikibooks.org/wiki/Algorithm_Implementation/Statistics/Fleiss%27_kappa#Python
and
http://john-uebersax.com/stat/raw.htm

"""

_author__ = "Luis Rei"
__copyright__ = "Copyright 2015 Luis Rei, Josef Stefan Institute, xLiMe"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "luis.rei@ijs.si"


import sys

DEBUG = False

def fleiss_kappa_interpret(kappa):
    """Return a string containing the human readable interpretation of the
    value of kappa.
    """

    if kappa >= 1.0:
        return "Perfect Agreement"
    if kappa > 0.8:
        return "Almost Perfect Agrement"
    if kappa > 0.6:
        return "Substantial Agreement"
    if kappa > 0.4:
        return "Moderate Agreement"
    if kappa > 0.2:
        return "Fair Agreement"
    if kappa > 0:
        return "Slight Agreement"
    
    return "Poor Agreement"


def compute_kappa(mat):
    """ Computes the Kappa value
        @param n Number of rating per subjects (number of human raters)
        @param mat Matrix[subjects][categories]
        @return The Kappa value """
    n = check_matrix(mat)   # PRE : every line count must be equal to n
    N = len(mat)
    k = len(mat[0])
    
    print n, "raters."
    print N, "subjects. (tokens/docs)"
    print k, "categories."
    
    # Computing p[]
    p = [0.0] * k
    for j in xrange(k):
        p[j] = 0.0
        for i in xrange(N):
            p[j] += mat[i][j]
        p[j] /= N*n
    if DEBUG: print "p =", p
    
    # Computing P[]    
    P = [0.0] * N
    for i in xrange(N):
        P[i] = 0.0
        for j in xrange(k):
            P[i] += mat[i][j] * mat[i][j]
        P[i] = (P[i] - n) / (n * (n - 1))
    if DEBUG: print "P =", P
    
    # Computing Pbar
    Pbar = sum(P) / N
    if DEBUG: print "Pbar =", Pbar
    
    # Computing PbarE
    PbarE = 0.0
    for pj in p:
        PbarE += pj * pj
    if DEBUG: print "PbarE =", PbarE
    
    kappa = (Pbar - PbarE) / (1 - PbarE)
    if DEBUG: print "kappa =", kappa
    
    return kappa


def raw_agreement_overall(mat):
    """the raw inter annotator agreement
    
    see http://john-uebersax.com/stat/raw.htm
    """
     # Note that notation here is different from fleiss function
    nk = check_matrix(mat)  # number of raters
    K = len(mat)            # number of subjects (cases)
    C = len(mat[0])         # number of categories
    
    S = [0.0] * K    # Total number of agreements on level (cat) j
    Sp = [0.0] * K   # Possible number of agreements on level (cat) j
    
    for k in range(K):
        for j in range(C):
            S[j] += mat[k][j] * (mat[k][j] - 1)
            
    O = sum(S)
    Op = nk * (nk - 1) * K
    Op = float(Op)

    po = O / Op
    
    return po


def check_matrix(mat):
    """ Assert that each line has a constant number of ratings
        @param mat The matrix checked
        @return The number of ratings
        @throws AssertionError If lines contain different number of ratings """
    n = sum(mat[0])
    
    msg = "Line count != %d (n value)." % n

    assert all(sum(line) == n for line in mat[1:]), msg
    return n


def load_iaaa(filepath):
    lines = []
    with open(filepath) as fin:
        lines = fin.readlines()
    lines = [x.split() for x in lines]
    
    n_subjects = len(lines[0])
    n_raters = len(lines) - 1

    # now we need to build a vocabulary to map categorical labels to columns
    vocab = []
    for ii in range(1, len(lines)):
        for jj in range(len(lines[ii])):
            vocab.append(lines[ii][jj])
    vocab = list(set(vocab))
    n_categories = len(vocab)

    # our matrix will be cols=categories (labels) rows=subjects (examples)
    mat = []
    for ii in range(n_subjects):
        mat.append([0] * n_categories)

    for ii in range(len(lines[0])):
        for coder in range(1, len(lines)):
            col = vocab.index(lines[coder][ii])
            row = ii
            mat[row][col] += 1
    
    return mat


def main():
    filename = sys.argv[1]
    print('------------------------')
    print('File: {}'.format(filename))
    print('------------------------')

    mat = load_iaaa(filename)

    kappa = compute_kappa(mat)
    kappa_str = fleiss_kappa_interpret(kappa)
    agr = raw_agreement_overall(mat)

    s = "agreement = {}\nfleiss kappa = {}\n{}".format(agr, kappa, kappa_str)
    print(s)


if __name__ == '__main__':
    main()
