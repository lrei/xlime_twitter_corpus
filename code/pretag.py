"""
Script for pre-tagging (POS) the xLiMe twitter corpus and generating the
data for loading by annotweb
"""

import gzip
import json
import argparse
import csv
import random
from pattern import it, es, de

(NOUN, VERB, ADJ, ADV, PRON, DET, PREP, ADP, NUM, CONJ, INTJ, PRT, PUNC, X) =\
    ("NN", "VB", "JJ", "RB", "PR", "DT", "PP", "PP", "NO", "CJ", "UH", "PT",
     ".", "X")
(HASHTAG, MENTION, URL, CONTINUATION) =\
    ("HASHTAG", "MENTION", "URL", "CONTINUATION")

tag2wordmap = {NOUN: "NOUN",
               VERB: "VERB",
               ADJ: "ADJECTIVE",
               'J': "ADJECTIVE",       # improperly tagged adjective
               ADV: "ADVERB",
               PRON: "PRONOUN",
               DET: "DETERMINER",
               PREP: "ADPOSITION",     # preposition -> adposition
               ADP: "ADPOSITION",      # [circ|pre|post]positions
               NUM: "NUMBER",          # cardinal numbers
               CONJ: "CONJUNCTION",
               INTJ: "INTERJECTION",
               PRT: "PARTICLE",
               PUNC: "PUNCTUATION",
               X: "OTHER",
               HASHTAG: HASHTAG,
               MENTION: MENTION,
               URL: URL,
               CONTINUATION: CONTINUATION}


def get_id_str(d):
    """
    Returns the document id or raises KeyError
    """
    if not 'id_str' and not 'id' in d:
        raise KeyError('id not in document')

    if 'id_str' in d:
        return d['id_str'].encode('utf8')

    return str(d['id'])


def get_tag_function(d):
    """
    Language Routing for PoS
    """
    if 'lang' not in d:
        raise KeyError('lang not in document')

    if d['lang'] == 'de':
        return de.tag
    elif d['lang'] == 'es':
        return es.tag
    elif d['lang'] == 'it':
        return it.tag

    raise NotImplementedError('document language not supported')


def tag_doc(d):
    """
    PoS tagging for a given document
    """
    if 'text' not in d:
        raise KeyError('text not in document')
    text = d['text'].encode('utf-8')

    doc_id = get_id_str(d)
    tag = get_tag_function(d)

    tagged = tag(text, tokenize=False, tagset='universal')
    tagged = [(word.encode('utf-8'), tag2wordmap[tt]) for word, tt in tagged]
    tagged = [{'doc_id': doc_id, 'tagged': tagged}]

    return tagged


def tag_file(infile, max_lines=10000):
    """
    Part of Speech Tagging for a file
    """
    tagged = []
    counter = 0
    with gzip.open(infile) as source:
        for line in source:
            if line.strip():
                counter += 1
                tagged.extend(tag_doc(json.loads(line)))
                if counter >= max_lines:
                    break
    return tagged


def xlime_easy_pos(token, tag):
    """
    Fix the PoS tag in some easy cases
    """
    tok = token.lower().strip()
    smileys = [':)', ':-)', ':(', ':-(']

    if tok == 'tuseruser':
        return 'MENTION'
    elif tok == 'turlurl':
        return 'URL'
    elif tok == 'rt':
        return 'CONTINUATION'
    elif tok.startswith('#'):
        return 'HASHTAG'
    elif tok in smileys:
        return 'EMOTICON'

    return tag


def convert_annot_xlime(tagged):
    """
    Convert to xLiMe annotweb format
    """
    # form a list of dictionaries
    ner_tags = ['B-PERSON', 'I-PERSON', 'B-ORG', 'I-ORG', 'B-MISC', 'I-MISC',
                'B-LOCATION', 'I-LOCATION', 'O']
    sentiment_classes = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']

    rows = []
    counter = 1
    for doc_tags in tagged:
        doc_id = doc_tags['doc_id']
        token_tags = doc_tags['tagged']

        for (token, tag) in token_tags:
            tok_id = doc_id + '-' + str(counter)
            counter += 1
            rows.append({'token': token,
                         'tok_id': tok_id,
                         'doc_id': doc_id,
                         'tok_task_pos': xlime_easy_pos(token, tag),
                         'tok_task_ner': 'O',
                         'doc_task_sentiment': 'NEUTRAL'})

    # fill tagset
    full_tagset = set(tag2wordmap.values())
    cur_tagset = set([r['tok_task_pos'] for r in rows])
    missing = full_tagset - cur_tagset
    if missing:
        for tag in missing:
            rid = random.randint(0, len(rows))
            rows[rid]['tok_task_pos'] = tag

    # fill ner
    cur_nerset = set([r['tok_task_pos'] for r in rows])
    full_nerset = set(ner_tags)
    missing = full_nerset - cur_nerset
    if missing:
        for tag in missing:
            for _ in range(10):
                rid = random.randint(0, len(rows))
                rows[rid]['tok_task_ner'] = tag

    # fill sentiment
    cur_sentiset = set([r['doc_task_sentiment'] for r in rows])
    full_sentiset = set(sentiment_classes)
    missing = full_sentiset - cur_sentiset
    if missing:
        for tag in missing:
            for _ in range(10):
                rid = random.randint(0, len(rows))
                rows[rid]['doc_task_sentiment'] = tag

    return rows


def write_file(data, outfile):
    """
    Write the tab sep file (tsv)
    """
    #fieldnames = data[0].keys()
    fieldnames = ['token', 'tok_id', 'doc_id', 'tok_task_pos', 'tok_task_ner',
                  'doc_task_sentiment']
    with open(outfile, 'w') as dest:
        writer = csv.DictWriter(dest, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(data)


def main():
    """
    main
    """
    limit = 10000
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='input file')
    parser.add_argument('output_file', help='output file')
    parser.add_argument('--limit', help='limit number of documents',
                        default=10000, type=int)
    args = parser.parse_args()

    infile = args.input_file
    outfile = args.output_file
    limit = args.limit

    print("%s -> %s (%d documents)" % (infile, outfile, limit))

    # tag
    tagged = tag_file(infile, limit)
    tagged = convert_annot_xlime(tagged)
    # write to csv
    write_file(tagged, outfile)


if __name__ == '__main__':
    main()
