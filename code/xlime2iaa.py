#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Converts an annotweb file to a columnar format that facilitates calculating IAA
measures

    annotator token1,1 token1,2 ...
    annotator1: label1,1,1 label1,2,1 ...
    annotator2: label1,1,2 label1,2,2 ...


Usage:

    python code/xlime2iaa.py [sent|pos|ner] data/[x].tsv corpus_task/[x]_[sent|pos|ner].iaa

"""

import sys
import pandas as pd
from data import *


usage = ("python code/xlime2iaa.py [sent|pos|ner] " + 
        "data/[x].tsv agreement/[x]_[sent|pos|ner].iaa")


def sentiment_iaa(data, annot_ids, doc_ids):
    outlabels = {}
    outtext = []

    print len(annot_ids), "raters."
    print len(doc_ids), "subjects. (docs)"

    for annot_id in annot_ids:
        outlabels[annot_id] = []

    for doc_id in doc_ids:
        outtext.append(doc_id)
        doc_data = data[data.doc_id == doc_id]

        for annot_id in annot_ids:
            doc_data_a = doc_data[doc_data.annotator == annot_id]
            sentiment = list(set(doc_data_a.doc_task_sentiment))[0].lower()
            outlabels[annot_id].append(sentiment)

    return outlabels, outtext


def tok_iaa(data, annot_ids, tok_ids, col):
    outlabels = {}
    outtext = []

    print len(annot_ids), "raters."
    print len(tok_ids), "subjects. (tokens)"

    for annot_id in annot_ids:
        outlabels[annot_id] = []

    for tok_id in tok_ids:
        # Get the token
        tok_data = data[data.tok_id == tok_id]
        token = list(set(tok_data['token']))[0]
        outtext.append(token)

        for annot_id in annot_ids:
            tok_data_a = tok_data[tok_data.annotator == annot_id]
            lbl = list(set(tok_data_a[col]))[0].upper()
            if '-' in lbl:
                # remove prefix
                lbl = lbl.split('-')[1]  
            outlabels[annot_id].append(lbl)

    return outlabels, outtext


SENTIMENT = False
if sys.argv[1] == 'sent':
    col = 'doc_task_sentiment'
    SENTIMENT = True
else:
    col = 'tok_task_' + sys.argv[1]

infile = sys.argv[2]
outfile = sys.argv[3]

# read file
data = pd.read_csv(infile, sep='\t')

# remove overlap (even if they match)
data = corpus_filter_common_docs(data)

# sort by token id
data.sort('tok_id', inplace=True)

annot_ids = list(set(data['annotator']))
doc_ids = list(set(data['doc_id']))
tok_ids = list(set(data['tok_id']))


# for each document
if SENTIMENT: 
    outlabels, outtext = sentiment_iaa(data, annot_ids, doc_ids)
else:
    outlabels, outtext = tok_iaa(data, annot_ids, tok_ids, col)


with open(outfile, 'w') as aout:
    line = ""
    for tid in outtext:
        line = line + str(tid) + '\t'
    line = line.strip() + '\n'
    aout.write(line)

    for annot_id in annot_ids:
        line = ""
        annotations = outlabels[annot_id]
        for a in annotations:
            line = line + a + '\t'
        line = line.strip() + "\n"
        aout.write(line)

