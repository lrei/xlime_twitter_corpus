# Annotation Guidelines for the xLiMe Twitter Corpus

Version 1.0 Draft 3
Luis Rei, Simon Krek, Dunja Mladenić
AILab, Josef Stefan Institute
July 2015


## Part of Speech


### Introduction
The guidelines for PoS annotation for twitter are based on [1].
For Language Specific annotation guidelines refer to other documents [2, 3, 4].
Credit is also given to [5] which was influential in the creation of this tagset which mostly consists of combining [1] with [5].

All tags available to the annotators are pre-specified in this document.


###  Part of Speech Tags

	- Noun
	- Verb (Verb, Aux Verb)
	- Article
	- Adjective
	- Determiner
	- Pronoun
	- Adverb
	- Conjuntion
	- Particle (Particle, other function words)
	- Number (Cardinal)
	- Interjection
	- Adposition (Preposition/Postposition/Circumposition)
	- Punctuation
	- Other (Residual, Garbage, Foreign, Abbreviation, Clipped)


#### Punctuation

	!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~

Though some of these characters have twitter specific meanings or can be part
of a smiley or an arrow. In those cases refer to their respective sections.

They can also be an error either of the original tweet or of the tokenization process. In that case they are labeled “Other”.

If an elipsis ("...") or "<<" indicates continuation, it should be labeled "Continuation" not "Punctuation".


#### Metalinguistic Mentions
See Section 3.8 of [1].


#### Numbers
See Section 3.2 of [1].


#### German Guidelines
See Appendix A1 of the Tiger Tagset Guidelines [2].


#### Italian Guidelines
See Tanl Tagset [3].


#### Spanish Guidelines
See [4].


### Twitter specific Part of Speech Tags

	- Hashtag
	- Mention
	- URL (URL, E-Mail Address)
	- Continuation (Discourse Marker)

#### Notes on Preprocessing
In our case we have removed @mentions (replaced with the token TUSERTUSER) and detected URLs (replaced with TURL) i.e.

	"Hello @lmrei see this http://ailab.ijs.si"

became
	
	"Hello TUSERTUSER see this TURLURL"

These should be tagged "Mention" and "URL" respectively.



#### Tokenization
See section 2 of [1]. Tokenization errors in emoticons should also be tagged “Other”.


#### Hashtag and Symbols
Twitter [hashtags](https://support.twitter.com/articles/49309#) are usually irrelevant for the sentence construction but not always. Consider the following examples 1, 2, 3:
	
	1. "I love Slovenia #funandsun"
	2. "I went to #slovenia"
	3. "I #love Slovenia"

In the first case, simply use the "Hashtag" category for "funandsun". In the second and third cases, it is actually an essential part of the sentence and should be labelled "Noun" and "Verb" respectively i.e. the tag it would have if it were not a hashtag.


Twitter also uses [Symbols](https://dev.twitter.com/overview/api/entities-in-twitter-objects#symbols) which consist of the dollar sign followed by a stock ticker. For example:

	"We all buy a lot of $COKE"

The Symbol is usually a noun since it usually replaces the name of a company. As with Hashtags, use whatever part of speech is appropriate in the sentence and if none is appropriate, label it “Hashtag”.


#### Miscellanious Abbreviations
See section 4.2 of [1].
Common abbreviations such as "lol" or entities such as msft (abbreviation for microsoft should be tagged in their respective categories.


#### Clipping
See section 4.3 of [1].


#### Emoticons, At-Mention, URLs, RT
 Emoticons such as :-) have their own tag "Emoticon". For a list of emoticons see the [Wikipedia List of Emoticons](https://en.wikipedia.org/wiki/List_of_emoticons).


URLs and Emails addresses are both tagged "URL".


While URLs and Mentions can be identified from the twitter stream metadata, the same is not true for email addresses and emoticons. Neverthless regular expressions exist that can capture most of them easily.


#### Continuation
See section 4.5 of [1].

[Retweets](https://support.twitter.com/articles/77606-faqs-about-retweets-rt) are another important concept in tweets - these often start with the characters “RT” or “rt”. These are often, but not always, followed by a mention and “:”.  Examples:

	“RT Go Red Socks @lmrei”
	“rt @lmrei: not wearing red socks today” 



#### Spelling
See section 4.6 of [1].


#### Direct Address
See section 4.7 of [1].


#### Arrows
See [1]


### Other helpful resources
General: [Universal Dependencies](http://universaldependencies.github.io/docs/#language-)



## Named Entity Recognition

### Introduction
This task consists of identifying and categorizing words that are part of named entities. The types we have selected based on [6] are: Persons, Organizations, Locations and Miscellaneous. 

We use the *IOB* format where "I" stands for "Inside", "O" for "Outside" and "B" for "Begin". All tokens not part of a named entity labelled "O" ("Outside"). A token is marked "B" if it it marks the beginning of a named entity. Subsequent tokens within that name are tagged "I".

Example:
    
    Barack  B-PERSON 
    Obama   I-PERSON
    spoke   O 
    at      O
    the     O
    United  B-ORGANIZATION
    Nations I-ORGANIZATION
    in      O
    New     B-LOCATION
    York    I-LOCATION
    .       O
    
    Leonard     B-PERSON
    recently    O
    starred     O
    in          O
    the         O
    movie       O
    Wolf        B-MISCELLANEOUS
    of          I-MISCELLANEOUS
    Wall        I-MISCELLANEOUS
    Street      I-MISCELLANEOUS
    



### Named Entity Type List


**Locations**: 

 - roads (streets, motorways)
 - trajectories
 - regions (villages, towns, cities, provinces, countries, continents, dioceses, parishes)
 - structures (bridges, ports, dams)
 - natural locations (mountains, mountain ranges, woods, rivers, wells, fields, valleys, gardens,nature reserves, allotments, beaches,national parks)
 - public places (squares, opera houses, museums, schools, markets, airports, stations, swimming pools, hospitals, sports facilities, youth centers, parks, town halls, theaters, cinemas, galleries, camping grounds, NASA launch pads, club houses, universities, libraries, churches, medical centers, parking lots, playgrounds, cemeteries)
 - commercial places (chemists, pubs, restaurants, depots, hostels, hotels, industrial parks, nightclubs, music venues)
 - assorted buildings (houses, monasteries, creches, mills, army barracks, castles, retirement homes, towers, halls, rooms, vicarages, courtyards)
 - abstract ``places'' (e.g. *the free world*)


**Miscellaneous**: 
 
 - words of which one part is a location, organisation, miscellaneous, or person;
 - adjectives and other words derived from a word which is location, organisation, miscellaneous, or person;
 - religions
 - political ideologies
 - nationalities
 - languages
 - programs 
 - events (conferences, festivals, sports competitions, forums, parties, concerts)
 - wars 
 - sports related names (league tables, leagues, cups)
 - titles (books, songs, films, stories, albums, musicals, TV programs)
 - slogans
 - eras in time
 - types (not brands) of objects (car types, planes, motorbikes)


**Organizations**:

 - companies (press agencies, studios, banks, stock markets, manufacturers, cooperatives)
 - subdivisions of companies (newsrooms)
 - brands
 - political movements (political parties, terrorist organisations, 
 - government bodies (ministries, councils, courts, political unions of countries (e.g. the *U.N.*))
 - publications (magazines, newspapers, journals) musical companies (bands, choirs, opera companies, orchestras
 - public organisations (schools, universities, charities)
 - other collections of people (sports clubs, sports teams, associations, theaters companies, religious orders, youth organisations)

             
**Persons**: 

 - first, middle and last names of people, animals and fictional characters
 - aliases


### Twitter Specific Notes

If a named entity is part of a Hashtag, it should still be tagged as if it was a normal token e.g.:

```html
	“I went to #slovenia”
	“I watched the new #avengers movie today”
```

“#Slovenia” should be tagged B-LOCATION and “#avengers” as B-MISCELLANEOUS.


Mentions should be tagged "Outside" since they always represent a named entity and can be easily automatically tagged. Their category can generally be determined more accurately from profile information. The same applies to URLs.



## References
[1] [Annotation Guidelines for Twitter Part-of-Speech Tagging Version 0.3](http://www.ark.cs.cmu.edu/TweetNLP/annot_guidelines.pdf), March 2013, Kevin Gimpel Nathan Schneider Brendan O’Connor [http://www.ark.cs.cmu.edu/TweetNLP/]

[2] [A Brief Introduction to the TIGER Treebank, Version 1 George Smith, Universit ̈at Potsdam](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/annotation/tiger_introduction.pdf)

[3] [Tanl POS Tagset](http://medialab.di.unipi.it/wiki/Tanl_POS_Tagset)

[4] [Universal Dependencies: Spanish](http://universaldependencies.github.io/docs/es/pos/index.html)

[5] S. Petrov, D. Das, and R. McDonald.  2012.  A universal part-of-speech tagset. In Proc. of LREC 2012

[6] [CONLL 2003 NER](http://www.cnts.ua.ac.be/conll2003/ner/)
