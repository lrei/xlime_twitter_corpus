#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
stats.py
Extracts basic statistics from an xLiMe twitter corpus file.
Namely:
  - number of documents (tweets)
  - number of tokens
  - number of annotators
  - overlap between annotators in number of documents and tokens

Requirements (check requirements.txt for specific version):
    pandas: pip install pandas
"""

_author__ = "Luis Rei"
__copyright__ = "Copyright 2015 Luis Rei, Josef Stefan Institute, xLiMe"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "luis.rei@ijs.si"


import pandas as pd
from data import *


def corpus_stats_basic(df, verbose=True):
    """Number of Documents and Tokens in the loaded Corpus file

    Args:
        df: pandas dataframe obtained from pd.load_csv
        verbose: prints instead of just returning the values
    """
    
    n_docs = df['doc_id'].nunique()
    n_toks = df['tok_id'].nunique()
    n_annotators = df['annotator'].nunique()
    
    if verbose:
        print('Documents: {}\nTokens: {}\nAnnotators: {}'
              .format(n_docs, n_toks, n_annotators))
    
    return (n_docs, n_toks, n_annotators)


def corpus_overlap(df, verbose=True):
    """Overlap between annotators in number of documents and tokens

    Args:
        df: pandas dataframe obtained from pd.load_csv
        verbose: displays the overlap instead of just returning

    Return:
        tuple ([int], [int]) number of overlapping (documents, tokens)
    """

    common_docs = get_overlap_ids(df, 'doc_id')
    n_c_docs = len(common_docs)
    common_toks = get_overlap_ids(df, 'tok_id')
    n_c_toks = len(common_toks)
    
    if verbose:
        print('Overlap: {} (docs) {} (tokens)'.format(n_c_docs, n_c_toks))
        
    return (common_docs, common_toks)


def corpus_stats(filepath):
    """Displays all the defined corpus statistics for a given corpus file
        - number of documents
        - number of tokens
        - number of annotators
        - number of overlapping documents
        - number of overlapping tokens
    """
    print('File: {}'.format(filepath))
    data = pd.read_csv(filepath, sep='\t')
    # 1 - Calculate Total Docs / Tokens / Common
    n_docs, n_toks, n_annotators = corpus_stats_basic(data)
    common_docs, common_toks = corpus_overlap(data)


def main():
    file_spanish = "data/spanish_task_1440847551.tsv"
    file_italian = "data/italian_task_1442142987.tsv"
    file_german = "data/german_task_1442142996.tsv"
    corpus_files = [file_spanish, file_italian, file_german]

    print('')
    for fname in corpus_files:
        corpus_stats(fname)
        print('\n')


if __name__ == '__main__':
    main()

