'''
Converts an annotweb file to CONLL format for a given column
'''

import sys
import pandas as pd

col = 'tok_task_' + sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]


data = pd.read_csv(infile, sep='\t')
# sort by token id
data.sort('tok_id', inplace=True)
# get a list of annotators
annotators = list(set(data['annotator']))

# lists of lists (lists of tweet tokens or labels)
outlabels = {}
outtext = {}

# check if it has been 'seen' - annotated by multiple annotators
seen = set()

# for each annotator
for annotator in annotators:
    # get the annotations
    annotator_data = data[data.annotator == annotator]
    # list of documents for that annotator
    doc_ids = list(set(annotator_data['doc_id']))

    # for each document
    for doc_id in doc_ids:
        # get the document data
        doc_data = annotator_data[annotator_data.doc_id == doc_id]

        # list of tokens ids
        tok_ids = list(doc_data['tok_id'])

        # the doc id (i.e. tweet id)
        doc_id = list(set(doc_data.doc_id))[0]

        # remove documents with multiple annotators
        if doc_id in seen:
            if doc_id in outtext:
                del outlabels[doc_id]
                del outtext[doc_id]
            continue

        # add document to the seen set
        seen.add(doc_id)

        tokens = list(doc_data['token'])
        labels = list(doc_data[col])

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
