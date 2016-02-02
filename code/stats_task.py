#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
stats.py
Extracts task specific statistics from an xLiMe twitter corpus file.

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


def ner_remove_prefix(df):
    """ Remove the I/B prefix from ner
    """
    m = {'I-LOCATION': 'LOCATION',
         'B-LOCATION': 'LOCATION',
         'B-MISC': 'MISC',
         'I-MISC': 'MISC',
         'B-ORG': 'ORG',
         'I-ORG': 'ORG',
         'B-PERSON': 'PERSON',
         'I-PERSON': 'PERSON'}
    df['tok_task_ner'] = df['tok_task_ner'].map(m)
    return df


def corpus_task_stats(filename, tasks):
    lang = language_from_filename(filename)
    print('------------------------')
    print(lang)
    print('File: {}'.format(filename))
    print('------------------------')

    df = pd.read_csv(filename, sep='\t')
    for prp_id, prp_lbl in tasks:
        local_df = corpus_filter_not_common_docs(df, 'doc_id')
        if prp_lbl == 'tok_task_ner':
            local_df = ner_remove_prefix(local_df)
        local_df = local_df[[prp_lbl]].groupby(prp_lbl)[prp_lbl].count()
        print(local_df)
        print('\n')
     

def main():
    file_spanish = "data/spanish_task_1440847551.tsv"
    file_italian = "data/italian_task_1442142987.tsv"
    file_german = "data/german_task_1442142996.tsv"
    corpus_files = [file_spanish, file_italian, file_german]
    tasks = [('doc_id', 'doc_task_sentiment'), ('tok_id', 'tok_task_pos'),
             ('tok_id', 'tok_task_ner')]

    for fname in corpus_files:
        corpus_task_stats(fname, tasks)
        print('\n\n')


if __name__ == '__main__':
    main()
