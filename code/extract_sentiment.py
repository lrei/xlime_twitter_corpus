#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
extract_sentiment.py
Extracts sentiment corpus in the format id\t\text\tsentiment 
from the original corpus file.

Usage: 

    python code/extract_sentiment.py data/[x].tsv corpus_task/[x]_sentiment.tsv

"""


import sys
import csv
import pandas as pd
from data import corpus_filter_not_common_docs

infile = sys.argv[1]
outfile = sys.argv[2]

# read file
data = pd.read_csv(infile, sep='\t')

# remove overlap (even if they match)
data = corpus_filter_not_common_docs(data)

# sort by token id i.e. i want the tweet text to come out in the right order
data.sort('tok_id', inplace=True)

outdata = {}
outtext = {}

doc_ids = list(set(data['doc_id']))

# for each document
for doc_id in doc_ids:
    doc_data = data[data.doc_id == doc_id]
    # the list of tokens
    tokens = list(doc_data['token'])
    # which becomes the text
    outtext[doc_id] = ' '.join(tokens)

    # the id property
    doc_id = list(set(doc_data.doc_id))[0]

    # the value of the sentiment label
    doc_sentiment = list(set(doc_data.doc_task_sentiment))[0].lower()
    outdata[doc_id] = doc_sentiment

with open(outfile, 'w') as aout:
    aout.write('id\ttext\tlabel\n')
    for tid in outdata:
        aout.write('%d\t%s\t%s\n' % (tid, outtext[tid], outdata[tid]))
