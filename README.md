# xLiMe Twitter Corpus

Luis Rei, Simon Krek, Dunja Mladenić

{first.last}@ijs.si

## Overview

Languages:

* German
* Italian
* Spanish

Annotations:

* Part of Speech Tags
* Named Entities
* Sentiment (Polarity, Message Level)

### Overall Numbers

The corpus consists of annotated tweets.
Some tweets were set aside and labeled by all annotators working on the language.

| Language  | Number of Annotators | Tweets        | Tokens  | Overlapping Tweets | Overlapping Tokens |
| --------- | -------------------- | ------------- | ------- | ------------------ | ------------------ |
| German    | 2                    | 3447          | 58264   | 47                 | 791                |
| Italian   | 3                    | 8646          | 154371  | 45                 | 758                |
| Spanish   | 2                    | 7713          | 133906  | 45                 | 721                |


After removing the overlapping tweets the resulting corpus is

| Language     | Tweets | Tokens   |
| ------------ | ------ | -------- |
| German       | 3400   | 60873    |
| Italian      | 8601   | 162269   |
| Spanish      | 7668   | 140852   |


### Sentiment

| Language  | Positive | Neutral | Negative  | Total |
| --------- | -------- | ------- | --------- | ----- |
| German    | 334      | 2924    | 142       | 3400  |
| Italian   | 554      | 7524    | 523       | 8601  |
| Spanish   | 388      | 7083    | 197       | 7668  |


### Part of Speech

| Tag          | German   | Italian | Spanish   |
| ------------ | -------- | ------- | --------- |
| Adjective    | 2514     | 7684    | 5741      |
| Adposition   | 4333     | 14960   | 13467     |
| Adverb       | 4173     | 8476    | 6116      |
| Conjunction  | 1576     | 6737    | 6684      |
| Continuation | 918      | 4227    | 3422      |
| Determiner   | 2990     | 9811    | 10037     |
| Emoticon     | 449      | 1076    | 951       |
| Hashtag      | 1895     | 3035    | 1805      |
| Interjection | 225      | 1427    | 1109      |
| Mention      | 1984     | 6519    | 9070      |
| Noun         | 11057    | 30759   | 23230     |
| Number       | 1176     | 2550    | 1568      |
| Other        | 1936     | 1503    | 3033      |
| Particle     | 638      | 352     | 18        |
| Pronoun      | 4530     | 7737    | 10333     |
| Punctuation  | 8650     | 20529   | 14102     |
| URL          | 1923     | 4494    | 3019      |
| Verb         | 6506     | 21793   | 19460     |


### Named Entities

| Entity Type  | German | Italian | Spanish   |
| ------------ | ------ | ------- | ----------|
| Location     | 742    | 2087    | 1441      |
| Miscellaneous| 995    | 5802    | 775       |
| Organization | 350    | 1150    | 836       |
| Person       | 757    | 3701    | 2321      |
| Total        | 2844   | 12740   | 5373      |


## Agreement Measures

### Sentiment

| Measure             | German | Italian | Spanish |
| ------------------- | ------ | ------- | ------- |
| Number of Documents |  47    | 45      | 45      | 
| Number of Annotators|  2     | 3       | 2       | 
| Raw Agreement       |  0.83  | 0.59    | 0.73    |
| Cohen/Fleiss Kappa  | -0.07  | 0.02    | 0.37    |
| Interpretation      | Poor   | Slight  | Fair    |


### Part of Speech

| Measure              | German           | Italian         | Spanish           |
| -------------------- | ---------------- | --------------- | ----------------- |
| Number of Tokens     |  791             | 758             | 721               | 
| Number of Annotators |  2               | 3               | 2                 | 
| Raw Agreement        |  0.80            | 0.89            | 0.87              |
| Cohen/Fleiss Kappa   |  0.88            | 0.87            | 0.85              |
| Interpretation       | Almost Perfect   | Almost Perfect  | Almost Perfect    |


### Named Entity Recognition

| Measure              | German           | Italian         | Spanish           |
| -------------------- | ---------------- | --------------- | ----------------- |
| Number of Tokens     |  791             | 758             | 721               | 
| Number of Annotators |  2               | 3               | 2                 | 
| Raw Agreement        |  0.96            | 0.91            | 0.97              |
| Cohen/Fleiss Kappa   |  0.67            | 0.42            | 0.51              |
| Interpretation       | Substantial      | Moderate        | Moderate          |


## Collection and Preprocessing

The tweets were randomly sampled from the twitter public stream. They were 
preprocessed by the same preprocessing steps as in [twitter_sentiment_gen](https://github.com/lrei/twitter_sentiment_gen):

 1. Files no identified by twitter as part of the target language were
    discarded;
 2. Tweets with less than 5 tokens were discarded;
 3. Tweets with more than 3 mentions were discarded;
 4. Tweets with more than 2 URLs were discarded;
 5. [langid.py](https://github.com/saffsd/langid.py) [M11] was used on the tweet text without mentions or URLs and tweets with a target language  probability lower than 70% were discard;
 6. URLs and Mentions were replaced with a pre-specified token;
 7. Tweets were tokenized with a variant of twokenize [C10];
 8. For each language, a random subsample of 10,000 tweets was selected.


*Note*: Some errors seem to exist whereby some URLs are incorrectly tokenized.
This occurred *possibly* because of incorrect handling of truncated retweets.


## Annotation

The Part of Speech tags were pre-annotated using [Pattern](http://www.clips.ua.ac.be/pages/pattern) [S12].
The annotators used a web application that for each document allowed them to
perform both document level and token level annotations. The pre-annotation code
used is available in `code\pretag.py`.

The guidelines are available in the [Guidelines](guidelines.md) file.

Annotators had the option to mark any tweet as Trash (e.g. if the language was
misidentified) or Skip if they were unsure. The selection of a label was made via a "dropdown" menu with all possible options.

## Part of Speech (POS) Tagging Experiment

The baseline used for POS Tagging consists of a UniGram tagger implemented
with NLTK. The UniGram tagger assigns the most likely tag seen for a lower case
token in the training set if there are at least 5 examples. Otherwise it uses 
the most common tag ('NOUN'). Only universal tags were used in the training and
testing of this classifier in order to be comparable with the other classifiers.

The UniGram tagger is trained using the first 70% of the corpus and 
tested on the remaining 30%. This baseline tagger is contained in
`code/experiment.py`.

The other POS Taggers evaluated were:

 - [Stanford POS](http://nlp.stanford.edu/software/tagger.shtml) [T03]
 - [RDRPOSTagger](http://rdrpostagger.sourceforge.net/) [N14]


| Language  | Model                          | Accuracy | Tokens Evaluated |
| --------- |------------------------------- | -------- | ---------------- |
| German    | Baseline                       | 0.85     | 14106            |
| German    | Stanford POS (german-hgc)      | 0.69     | 47089            |
| German    | RDRPOSTagger (German)          | 0.70     | 47089            |
| Spanish   | Baseline                       | 0.89     | 31162            |
| Spanish   | Standord POS (spanish-distsim) | 0.13     | 103752           |
| Italian   | Baseline                       | 0.90     | 36708            |
| Italian   | RDRPOSTagger (Italian)         | 0.44     | 123080           |

The results obtained by the baseline were expected (see [C93]). The German
results  are only slightly lower than expected. The results obtained from
other taggers (Spanish and Italian) are significantly below our expectations. The two
hypothesis are that this was due to the difference in tagsets and tokenization. 

## Obtaining

[Download zip file](https://github.com/lrei/xlime_twitter_corpus/archive/master.zip).

or use git:

```bash
git clone https://github.com/lrei/xlime_twitter_corpus.git
```

## Files

### Directories

| Directory     | Description                                                             |
| ------------- | ----------------------------------------------------------------------- |
| data/         | Contains the original data exported from the annotation tool.           |
| code/         | Contains code for exporting the original data and calculating measures. |
| corpus\_task/ | Usable corpus (non-overlapping) by language and task.                   |
| agreement/    | Overlapping annotations in a format easy for calculating agreement.      |
| experiments/  | Contains the result of the POS tagging experiments.                     |


### Corpus - Usable (corpus\_task/)

The usable corpus consists of the tweets and their annotations, extracted from
the original data and converted into a more or less standard format using
scripts in the `code/` directory.

It does not include the overlapping tweets used to calculate agreement.

#### Sentiment

The sentiment files are in a Tab Separated Values format with the header:

```
id	text	label
```

 * **id** is the twitter provided tweet tweet id.
 * **text** is the text of the tweet
 * **label** is the manually assigned sentiment: 'positive', 'neutral' or 'negative'.

All instances of detected URLs have been replaced with the special token
*TURLTURL*. All instances of usernames have been replaced with *TUSERUSER*. 

These files were generated from the original data using the script
`code/extract_sentiment.py`.

#### Sequence Tagging: Part of Speech and Named Entity Recognition

The Part of Speech and Named Entity recognition files are in the CONLL format
which consists of empty-line delimited sentences (in this case, tweets) where
each non-empty line is a token followed by a space and the tag.



These files were generated from the original data using the script
`code/xlime2conll.py`

All instances of detected URLs have been replaced with the URL
*http://luisrei.com* and all instances of twitter username have 
*@lmrei*.

### Code
Running the code requires python and the pandas library.
The scripts are meant to be run from the base directory.
`twokenize.py` and `pretag.py` are include for reference and are not meant to be
run with the provided data.

Running `experiments.py` required a particular arrangement of the external
dependencies (Stanford POS Tagger and RDRPOSTagger).


```bash
git clone https://github.com/lrei/xlime_twitter_corpus.git
cd xlime_twitter_corpus
python code/stats.py
```

| File                 | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| agreement.py         | calculates the inter annotator agreement measures.                   |
| data.py              | common data manipulation functions used from other scripts.          |
| experiment.py        | runs the Part of Speech experiment.                                  |
| extract_sentiment.py | creates the sentiment corpus files from the original data.           |
| pretag.py            | was used to pre-annotate the corpus.                                 |
| seq.py               | contains several sequence tagging helper functions.                  |
| stats.py             | calculates the corpus token and document counts.                     |
| stats_task.py        | calculates the task specific counts.                                 |
| twokenize.py         | the tokenizer used in creating this corpus.                          |
| xlime2conll.py       | creates the POS and NER corpus from the original data.               |
| xlime2iaa.py         | saves the overlapping data in a format appropriate for`agreement.py` |


## Guidelines

The guidelines are available at [Guidelines](guidelines.md).


## Acknowledgments
The annotators, in alphabetical order: Edvin Dervisevic, Miha Helbl, Jošt Jesenovec, Maša Kmet, Eva Podobnik, Iza Škrjanec and Viktor Zelj.

This work was supported by the Slovenian Research Agency and the ICT Programme of the EC under XLime (FP7-ICT-611346). 

## References

[C93] Eugene Charniak, Curtis Hendrickson, Neil Jacobson, and Mike Perkowitz. 1993. Equations for part-of-speech tagging. In AAAI, pages 784–789. 

[T03] Kristina Toutanova, Dan Klein, Christopher Manning, and Yoram Singer. 2003. Feature-Rich Part-of-Speech Tagging with a Cyclic Dependency Network. In Proceedings of HLT-NAACL 2003, pp. 252-259

[C10] TweetMotif: Exploratory Search and Topic Summarization for Twitter. Brendan O'Connor, Michel Krieger, and David Ahn. ICWSM-2010 (demo track). http://brenocon.com/oconnor_krieger_ahn.icwsm2010.tweetmotif.pdf

[M11] Lui, Marco and Timothy Baldwin (2011) Cross-domain Feature Selection for Language Identification, In Proceedings of the Fifth International Joint Conference on Natural Language Processing (IJCNLP 2011), Chiang Mai, Thailand, pp. 553—561. http://www.aclweb.org/anthology/I11-1062

[S12] De Smedt, T. & Daelemans, W. (2012). Pattern for Python. Journal of Machine Learning Research, 13: 2031–2035.

[N14] Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham and Son Bao Pham. RDRPOSTagger: A Ripple Down Rules-based Part-Of-Speech Tagger. In Proceedings of the Demonstrations at the 14th Conference of the European Chapter of the Association for Computational Linguistics (EACL), pp. 17-20, 2014. http://www.aclweb.org/anthology/E14-2005
