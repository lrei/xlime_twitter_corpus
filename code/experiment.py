#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
POS Tagging Experiment
"""

import sys
import time
from seq import *


STANFORD_POS_PATH = './stanford/stanford-postagger-3.5.2.jar'
MODELS = {
        'de':'./stanford/models/german-hgc.tagger',
        'es':'./stanford/models/spanish-distsim.tagger',
        'it':'./rdrpostagger/Models/POS/Italian.RDR',
        'de2':'./rdrpostagger/Models/POS/German.RDR',
        }
TAGSETS = {
        'de': 'de-negra',
        'de2': 'de-negra',
        'es': 'es-cast3lb',
        'it': 'it-isst',
        }

_UNI = ('VERB','NOUN','PRON','ADJ','ADV','ADP','CONJ','DET','NUM','PRT','X','.')


def gen_eval(model, tagged_sentences, whitelist=_UNI):
    gold = []
    pred = []
    toks = []
    total = len(tagged_sentences)
    count = 0
    start = time.time()
    last_pct = 0

    # For each sentence
    for tagged_sentence in tagged_sentences:
        # get tokens and gold tags
        tokens = [x[0] for x in tagged_sentence]
        toks += tokens
        gold += [x[1] for x in tagged_sentence]

        # tag the tokens, extract the tags list 
        tagged = model.tag(tokens)
        pred += [x[1] for x in tagged]
        count += 1
        pct = int( (count/float(total)) * 100 )
        if pct % 5 == 0 and pct != last_pct:
            last_pct = pct
            el = time.time() - start
            speed =  count / el
            eta = int((total - count) / speed)
            el = int(el)
            m = '{}s: {}/{} docs, {}%, eta={}s'
            m = m.format(el, count, total, pct, eta)
            print(m)

    el = time.time() - start
    avg_speed = len(gold) / el 
    m = '{} tokens in {}s -> avg speed: {} toks/s'
    m = m.format(len(gold), int(el), avg_speed)
    print(m)


    assert len(gold) == len(pred), "pred and gold are not the same length"
    assert len(gold) == len(toks), "tokebs and gold are not the same length"

    # remove from both tag lists where gold contains other tags
    # e.g. non-universal pos tags
    gold_new = []
    pred_new = []
    toks_new = []
    for ii in range(len(gold)):
        if gold[ii] in _UNI:
            gold_new.append(gold[ii])
            pred_new.append(pred[ii])
            toks_new.append(toks[ii])
    gold = gold_new
    pred = pred_new
    toks = toks_new

    return toks, gold, pred


def baseline(tagged_sentences):
    from nltk.tag import UnigramTagger
    from nltk.tag import DefaultTagger
    from collections import Counter

    # lowercase everything
    # remove all instances of non-universal tags for propper comparison with
    # the other methods
    new_tagged_sentences = []
    for sent in tagged_sentences:
        sent = [(x[0].lower(), x[1]) for x in sent]
        sent = [x for x in sent if x[1] in _UNI]
        new_tagged_sentences.append(sent)
    tagged_sentences = new_tagged_sentences

    # size of corpus
    corpus_size = sum([len(sent) for sent in tagged_sentences])
    print('Corpus size: {} docs'.format(len(tagged_sentences)))
    print('Corpus size: {} tokens'.format(corpus_size))
    
    # train/test split
    test_pct = 0.3
    test_len = int(len(tagged_sentences) * test_pct)
    test_idx = len(tagged_sentences) - test_len
    train_set = tagged_sentences[:test_idx]
    test_set = tagged_sentences[test_idx:]
    print('Train set: {} docs'.format(len(train_set)))
    print('Test set: {} docs'.format(len(test_set)))

    # calculate test set size in tokens
    test_size = sum([len(sent) for sent in test_set])
    print('Test set: {} tokens'.format(test_size))

    # calculate most comman tag in the train set
    # this should be 'NOUN'
    tag_dist = []
    for sent in train_set:
        tag_dist += [x[1] for x in sent]
    counts = Counter()
    counts.update(tag_dist)
    most_common = counts.most_common(1)[0][0]
    print('Most common tag: {}'.format(most_common))

    # Create model
    backoff = DefaultTagger(most_common)
    tagger = UnigramTagger(train=train_set, backoff=backoff, cutoff=5)

    # Evaluate
    acc = tagger.evaluate(test_set)
    print('Baseline: {}'.format(acc))


def main():
    lang = sys.argv[1]
    goldfile = sys.argv[2]
    resfile = sys.argv[3]

    print('--------------------')
    print('lang = {}'.format(lang))
    print('gold file = {}'.format(goldfile))
    print('--------------------')

    # Load the model
    model = load_pos(STANFORD_POS_PATH, MODELS[lang], TAGSETS[lang])

    # load gold set
    tagged_sentences = load_seq_file(goldfile)
    print('tagged tweets: {}'.format(len(tagged_sentences)))

    # Baseline
    baseline(tagged_sentences)

    # get data: tokens, gold tags, predicted tags
    toks, gold, pred = gen_eval(model, tagged_sentences)
    print('evaluation total: {}'.format(len(gold)))

    # save data
    save_eval(toks, pred, gold, resfile)

    # eval
    answers = []
    for ii in range(len(gold)):
        if pred[ii] == gold[ii]:
            answers += [1]
        else:
            answers += [0]
    acc = sum(answers) / float(len(answers))
    print(acc)


if __name__ == '__main__':
    main()
