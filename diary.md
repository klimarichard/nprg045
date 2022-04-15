# Work diary

***EWT** = estimated work-time in minutes*

**Total working-time:** 1215 minutes *(20:15 hours)*

## 29th March 2022, 21:30

- [x] created Git repository
- [x] added assignment description
- [x] added unpacked PDT data for parsing to <code>res</code> folder

**EWT:** 180 min.

## 30th March 2022, 12:30

- [x] created <code>src</code> folder
- [x] created <code>id_parser.py</code> file for parsing sentence IDs from PDT data
    - [x] parsing raw XML files and searching for IDs
    - [x] making parsing procedures for <code>m</code> and <code>a</code> files

**EWT:** 90 min.

## 31st March 2022, 18:30

- [x] sorting IDs and comparing ID lists from <code>m</code> and <code>a</code> type files
- [x] saving final list of IDs present in both type of files to <code>sentence_IDs_all.txt</code> file

#### Notes

- some source <code>m</code> files will be obsolete, since there are no <code>a</code> files for them to pair
- PC breakdown at 20:15 (new changes committed but not pushed)
    - data successfully recovered on 1st April 2022, 9:30

**EWT:** 105 min.

## 1st April 2022, 12:00

- [x] created <code>sentence_parser.py</code> file
- [ ] parsing sentences from ID list
    - [x] parsing sentences from <code>m</code> type files
    - [ ] parsing sentences from <code>a</code> type files *(not finished)*
- [x] save both <code>m</code> and <code>a</code> type IDs to files
    - <code>sentence_IDs_m.txt</code> and <code>sentence_IDs_a.txt</code> respectively

#### Notes

- parsing <code>a</code> type files requires a different approach
    - files are organized recursively into trees (<code>iter</code> method has to be used)
- is it needed to parse syntactical files?
    - maybe the constituent type is not needed, in which case the <code>a</code> type files are obsolete
    - it can be interesting to compare, if a tag based on the constituent type would improve the performance of the
      final model

**EWT:** 220 min.

## 4th April 2022, 14:45

- [x] parsing sentences from ID list
    - [x] parsing sentences from <code>a</code> type files
- [x] determining file format for saving parsed sentences
- [x] saving parsed sentences to <code>sentences_no_comma.txt</code> and <code>sentences_comma.txt</code> files

#### Notes

- the file format for parsed sentences was determined as:
    - each sentence is on multiple lines
    - the first line contains the sentence ID
    - the following lines contain the single words with their properties separated with tabs:
        - the word order in the sentence
        - the actual word
        - morphological tags for the word
        - constituent type of the word
    - sentences are divided by a single empty line

**EWT:** 180 min.

## 4th April 2022, 21:15

- [x] reorganizing files to store reusable functions in one place (creating <code>rikli</code> package)

#### Notes

- the idea behind this is to move reusable function into a package-like folder <code>rikli</code>
- more and more functions should be added to the files in this package during development

**EWT:** 60 min.

## 6th April 2022, 17:00

- [x] moving reusable functions into one package
- [x] mapping parsers to new locations of functions

**EWT:** 30 min.

## 6th April 2022, 18:30

- [x] correcting type-hints to Python standards
- [x] sentence loading redone and moved to the <code>rikli</code> package
- [x] first dummy version of <code>sentence_tagger</code>

**EWT:** 80 min.

## 7th April 2022, 13:30

- [x] automatized counting of total time in diary (in git ignored script)

**EWT:** 30 min.

## 7th April 2022, 15:30

- [x] basic version of sentence tagging
- [x] updated sentence printing

**EWT:** 120 min.

## 7th April 2022, 18:30

- [x] added <code>doc</code> folder
    - [x] added Positional Tags Quick Reference from prof. Hajič
        - replacing unknown Czech characters in the document

**EWT:** 30 min.

## 8th April 2022, 13:00

- [x] adjustments to sentence printing
- [x] adjustments to sentence tagging

**EWT:** 60 min.

## 15th April 2022, 14:30

- [x] adjustments to sentence tagging
- [x] first version of tagged sentences saved to file

**EWT:** 30 min.
