# xLiMe Twitter Corpus

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
Some tweets were set asside and labelled by all annotators working on the language.

| Language  | Number of Annotators | Tweets        | Tokens  | Overlapping Tweets | Overlapping Tokens |
| --------- | -------------------- | ------------- | ------- | ------------------ | ------------------ |
| German    | 2                    | 3447          | 58264   | 47                 | 791                |
| Italian   | 3                    | 8646          | 154371  | 45                 | 758                |
| Spanish   | 2                    | 7713          | 133906  | 45                 | 721                |


After removing the overlapping tweets the resulting corpus is

| Language     | Tweets | Tokens   |
| ------------ | ------------------|
| German       | 3400   | 60873    |
| Italian      | 8601   | 162269   |
| Spanish      | 7668   | 140852   |


### Sentiment

| Language  | Positive | Neutral | Negative  | Total |
| --------- | ------------------ | ----------|------ |
| German    | 334      | 2924    | 142       | 3400  |
| Italian   | 554      | 7524    | 523       | 8601  |
| Spanish   | 388      | 7083    | 197       | 7668  |


### Part of Speech

| Tag          | German   | Italian | Spanish   |
| ------------ | ------------------ | ----------|
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
| ------------ | ---------------- | ----------|
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


### NER

| Measure              | German           | Italian         | Spanish           |
| -------------------- | ---------------- | --------------- | ----------------- |
| Number of Token  s   |  791             | 758             | 721               | 
| Number of Annotators |  2               | 3               | 2                 | 
| Raw Agreement        |  0.96            | 0.91            | 0.97              |
| Cohen/Fleiss Kappa   |  0.67            | 0.42            | 0.51              |
| Interpretation       | Substantial      | Moderate        | Moderate          |




## Obtaining

[Download zip file]().

or use git:

```bash
git clone 
```


### Data Format

### Guidelines


## Running the code

Running the code requires python and the pandas library.

The scripts are meant to be run from the base directory.

```bash
git clone
cd xlime_twitter_corpus
python code/stats.py
```

### Description

#### code/stats.py

### code/agreement.py

## Running the experiments




## Acknowledgments
Annotators
