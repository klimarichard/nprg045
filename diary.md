# Work diary
***EWT** = estimated work-time in minutes*

**Total working-time:** 595 minutes *(9:55 hours)*

## 29th March 2022, 21:30

- [x] created Git repository
- [x] added assignment description
- [x] added unpacked PDT data for parsing to <code>res</code> folder

**EWT:** 180

## 30th March 2022, 12:30

- [x] created <code>src</code> folder
- [x] created <code>id_parser.py</code> file for parsing sentence IDs from PDT data
    - [x] parsing raw XML files and searching for IDs
    - [x] making parsing procedures for <code>m</code> and <code>a</code> files

**EWT:** 90

## 31st March 2022, 18:30

- [x] sorting IDs and comparing ID lists from <code>m</code> and <code>a</code> type files
- [x] saving final list of IDs present in both type of files to <code>sentence_IDs_all.txt</code> file

#### Notes
- some source <code>m</code> files will be obsolete, since there are no <code>a</code> files for them to pair
- PC breakdown at 20:15 (new changes committed but not pushed)
    - data successfully recovered on 1st April 2022, 9:30

**EWT:** 105

## 1st April 2022, 12:00

- [x] created <code>sentence_parser.py</code> file
- [ ] parsing sentences from ID list
    - [x] parsing sentences from <code>m</code> type files
    - [ ] parsing sentences from <code>a</code> type files
- [x] save both <code>m</code> and <code>a</code> type IDs to files
    - <code>sentence_IDs_m.txt</code> and <code>sentence_IDs_a.txt</code> respectively

#### Notes
- parsing <code>a</code> type files requires a different approach
    - files are organized recursively into trees (<code>iter</code> method has to be used)
- is it needed to parse syntactical files?
    - maybe the constituent type is not needed, in which case the <code>a</code> type files are obsolete
    - it can be interesting to compare, if a tag based on the constituent type would improve the performance of the
final model

**EWT:** 220

## Next steps
- determining file format for saving parsed sentences
- saving parsed sentence to <code>sentences_no_comma.txt</code> and <code>sentences_comma.txt</code> files