# -*- coding: utf8 -*-
"""
data.py
common data manipulation functions
"""

import os


def get_overlap_ids(df, id_prp='doc_id'):
    """Returns ids that overlap for all annotators given an id property

    Args:
        df: pandas dataframe obtained from pd.load_csv
        id_prp: property to use for calculating overlap: doc_id or tok_id

    Returns:
        [int] number of overlapping instances
    """
    common = set()
    flag_first = True
    annotators = df['annotator'].unique()

    for annotator in annotators:
        adf = df[df['annotator'] == annotator]
        ids = list(adf[id_prp])
        if flag_first:
            common = set(ids)
            flag_first = False
        else:
            common = common.intersection(set(ids))
    return common


def corpus_filter_common_docs(df, id_prp='doc_id'):
    """Returns the corpus with only documents (or tokens) which are common 
    to all annotators.
    """
    common_ids = list(get_overlap_ids(df, id_prp))
    fdf = df[df[id_prp].isin(common_ids)]
    return fdf


def corpus_filter_not_common_docs(df, id_prp='doc_id'):
    """Returns the corpus with only documents (or tokens) which are NOT common 
    to all annotators.
    """
    common_ids = set(list(get_overlap_ids(df, id_prp)))
    all_ids = set(list(df[id_prp]))
    not_common_ids = all_ids - common_ids
    
    fdf = df[df[id_prp].isin(not_common_ids)]
    
    return fdf


def language_from_filename(filename):
    return os.path.split(filename)[-1].split('_')[0].title()
