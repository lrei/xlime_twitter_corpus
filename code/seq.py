# -*- coding: utf-8 -*-
"""
Twitter Annotator Wrapper for Stanford NER/POS
Requires
nltk.download('universal_tagset')
"""

_author__ = "Luis Rei"
__copyright__ = "Copyright 2015 Luis Rei, Josef Stefan Institute, xLiMe"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "luis.rei@ijs.si"


import os
from nltk.tag import StanfordNERTagger, StanfordPOSTagger, map_tag
try:
    from SCRDRlearner.Object import FWObject
    from SCRDRlearner.SCRDRTree import SCRDRTree
    from SCRDRlearner.Utils import getWordTag, readDictionary
    from SCRDRlearner.InitialTagger import initializeSentence
except:
    print("can't import RDRPOSTagger")
    pass


class RDRPOSTagger(SCRDRTree):
    """
    RDRPOSTagger for a particular language
    """
    def __init__(self, model_path):
        self.root = None
        self.constructSCRDRtreeFromRDRfile(model_path)

        dict_path = os.path.split(model_path)[0]
        fname = os.path.split(model_path)[1]
        fname = fname.split('.')[0] + '.DICT'
        dict_path = os.path.join(dict_path, fname)
        self.DICT = readDictionary(dict_path)
    
    def tag(self, tokens):
        tokens = ' '.join(tokens)
        line = initializeSentence(self.DICT, tokens)
        sen = []
        wordTags = line.split()
        for i in xrange(len(wordTags)):
            fwObject = FWObject.getFWObject(wordTags, i)
            word, tag = getWordTag(wordTags[i])
            node = self.findFiredNode(fwObject)

            if node.depth > 0:
                sen.append((word, node.conclusion))
            else:# Fired at root, return initialized tag
                sen.append((word, tag))
        return sen


class POSModelWrapper():
    '''A lightwight wrapper for PoS models to convert their tags to the
    universal tagset if the tagmap parameter is passed

    E.g.
    German: de-negra (for the german-hgc model in stanford pos tagger)
    English: en-ptb (for the english stanford ner model)
    Spanish: es-cast3lb (ancora for the spanish model in stanford pos tagger)

    '''
    def __init__(self, model, tagmap=None):
        self.model = model
        self.tagmap = tagmap

    def tag(self, tokens):
        tagged = self.model.tag(tokens)

        if not self.tagmap:
            return tagged

        return [(word, map_tag(self.tagmap, 'universal', tag)) 
                for word, tag in tagged]


def rechunk(ner_output):
    '''Converts
    [(u'New', u'LOCATION'), (u'York', u'LOCATION'),(u'City', u'LOCATION')]
    to
    [(u'New York City', u'LOCATION')]

    "chunky" output from NER 
    - copied from http://stackoverflow.com/questions/27629130/
    '''
    chunked, tag = [], ''
    for i, word_tag in enumerate(ner_output):
        word, tag = word_tag
        if tag != u'O' and tag == prev_tag:
            chunked[-1] += word_tag
        else:
            chunked.append(word_tag)
        prev_tag = tag

    clean_chunked = [tuple([" ".join(wordtag[::2]), wordtag[-1]]) 
                    if len(wordtag)!=2 else wordtag for wordtag in chunked]

    return clean_chunked


def load_ner(tagger_path, model_path):
    return StanfordNERTagger(model_path, tagger_path, 'utf8')


def ner_tag(model, tokens):
    '''Returns is a list of word-tag pairs
    '''
    if model:
        return rechunk(model.tag(tokens))


def load_pos(tagger_path, model_path, tagset):
    # detect model type
    if model_path.endswith('RDR'):
        return POSModelWrapper(RDRPOSTagger(model_path), tagset)
    else:
        return POSModelWrapper(StanfordPOSTagger(model_path, tagger_path, 
                                                 'utf8'), tagset)


def pos_tag(model, tokens):
    if model:
        return model.tag(tokens)


def save_eval(tokens, pred, gold, filepath):
    '''Saves predicted and gold to a file in an easy-to-process format
    token1\ttoken2\t...\n
    gold1\tgold2\t...\n
    pred1\tpred2\t...\n
    '''

    def save_list(values, fout):
        s = ''
        for x in values:
            s += x + '\t'
        s = s.strip() + '\n'
        fout.write(s)
 

    with open(filepath, 'w') as fout:
        save_list(tokens, fout)
        save_list(gold, fout)
        save_list(pred, fout)


def load_seq_file(filepath):
    sentences = []
    sentence = []

    doc_count = 0
    tagged_count = 0

    with open(filepath) as fin:
        for line in fin:
            # handle sentence separator
            if not line.strip():
                doc_count += 1
                # empty line is a sentence (tweet/doc) separator
                if sentence:
                    sentences.append(sentence)
                sentence = []
                continue # new sentences

            # handle normal line
            tagged_count += 1
            word, label = line.strip().split()
            sentence.append((word, label))

    # final sentence
    if sentence:
        doc_count += 1
        sentences.append(sentence)

    #print(doc_count)
    #print(tagged_count)

    return sentences
