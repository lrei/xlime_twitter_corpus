#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Converts an annotweb file to CONLL format for a given column
Where by CONLL format I mean space delimited columns with the first column
being the token, the second column being the label and empty lines delimiting 
sentences.

    token1,1 -space- label 
    token1,2 -space- label 
    ...

    token1,2 -space- label 
    token2,2 -space- label 
    ...


Usage:

    python code/xlime2conll.py [pos|ner] data/[x].tsv corpus_task/[x]_[pos|ner].conll

"""

import sys
import pandas as pd
from data import *

m2short = {
        'VERB': 'VERB',
        'NOUN': 'NOUN',
        'PRONOUN': 'PRON',
        'ADJECTIVE':'ADJ',
        'ADVERB': 'ADV',
        'ADPOSITION': 'ADP',
        'CONJUNCTION': 'CONJ',
        'DETERMINANT': 'DET',
        'NUMBER': 'NUM',
        'PARTICLE':'PRT',
        'OTHER': 'X',
        'PUNCTUATION': '.',
        'HASHTAG': '#',
        'MENTION': '@',
        'URL': 'U',
        'CONTINUATION': '~',
        'EMOTICON': 'E'
        }

def tag2short(tag):
    tag = tag.upper()
    if tag in m2short:
        tag = m2short[tag]

    return tag


def replace_tokens(tokens):
    tokens_new = []
    for token in tokens:
        if token.lower() == 'tuseruser':
            token = '@lmrei'
        elif token.lower() == 'turlturl':
            token = 'http://luisrei.com'

        tokens_new.append(token)
    return tokens_new

col = 'tok_task_' + sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

# read file
data = pd.read_csv(infile, sep='\t')

# remove overlap (even if they match)
data = corpus_filter_not_common_docs(data)

# sort by token id
data.sort('tok_id', inplace=True)

# lists of lists (lists of tweet tokens or labels)
outlabels = {}
outtext = {}

doc_ids = list(set(data['doc_id']))

# check if it has been 'seen' - annotated by multiple annotators
seen = set()

# for each document
for doc_id in doc_ids:
    # get the document data
    doc_data = data[data.doc_id == doc_id]

    # list of tokens ids
    tok_ids = list(doc_data['tok_id'])

    # the doc id (i.e. tweet id)
    doc_id = list(set(doc_data.doc_id))[0]

    tokens = list(doc_data['token'])
    tokens = replace_tokens(tokens)
    labels = list(doc_data[col])
    # remove ner prefix if it is in there
    labels = [x.split('-')[1] if '-' in x else x for x in labels]
    # convert tags to short form
    if sys.argv[1] == 'pos':
        labels = [tag2short(x) for x in labels]

    outtext[doc_id] = tokens
    outlabels[doc_id] = labels


with open(outfile, 'w') as aout:
    # this would be the header but we don't use it
    # id could also be added to the output (tid)
    # aout.write('text\tlabel\n')
    for doc_id in outtext:
        tokens = outtext[doc_id]
        labels = outlabels[doc_id]

        for jj in range(len(tokens)):
            aout.write('%s %s\n' % (tokens[jj], labels[jj]))
            aout.flush()
        # end of sentence - empty line
        aout.write('\n')
