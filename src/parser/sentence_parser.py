import re
import xml.etree.ElementTree as ET


from src.rikli.file import read_ids_from_file
from src.rikli.file import get_pdt_folder


def parse_sentences(filename: str):  # -> [(str, [(int, str, str, str)])]:
    """
    Parses all sentences from corresponding m- and a-files and processes them to chosen format.
    The chosen format is a list of sentences, where each sentence is a tuple of ID and a list of words,
    where each word is a quadruple containing word order in sentence, the actual word, constituent type,
    and a string with tags.
    :param filename: name of XML files (without extension) with annotated data
    :return: list of sentences in chosen format
    """
    # Get parsed sentences from both morphological and syntactical data files
    sentences_m = parse_m_sentences(filename)
    sentences_a = parse_a_sentences(filename)

    sentences = [[id_a, join_word_properties(words_a, words_m)]
                 for id_a, words_a in sentences_a
                 for id_m, words_m in sentences_m
                 if id_a == id_m]

    return sentences


def parse_a_sentences(filename: str) -> [(str, [(str, int, str)])]:
    """
    Parses all sentences from one a-file and processes them to chosen format. This is a helper
    function for ``parse_sentences`` function. The chosen format is a list of sentences, where
    each sentence is a tuple of ID and a list of words, where each word is a triple containing
    the word ID, the order of the word in the sentence, and the constituent type of the word.
    :param filename: name of XML file with syntactically annotated data
    :return: list of sentences in chosen format
    """
    # Initializing sentences list
    sentences = []

    # Initializing XML parser
    xml_a = ET.parse(resdir + r'\unpacked_a' + '\\' + filename + '.a')
    trees = xml_a.find('{http://ufal.mff.cuni.cz/pdt/pml/}trees')
    lms = trees.findall('{http://ufal.mff.cuni.cz/pdt/pml/}LM')

    # for each sentence tree
    for lm in lms:
        # ID starts with "a-", which is only an indicator of the analytical file,
        # we only want the ID itself
        sentence_id = lm.get('id')[2:]

        # Recursively find all LM tags in this subtree (sentence)
        word_lms = lm.iter('{http://ufal.mff.cuni.cz/pdt/pml/}LM')

        # Initializing list of words in one sentence
        words = []
        for word in word_lms:
            word_id = word.get('id').split('-')[3]
            word_order, constituent = 0, None

            for elem in word:
                if re.match('.*ord$', elem.tag):
                    # writing the word order
                    word_order = int(elem.text)
                if re.match('.*afun$', elem.tag):
                    # writing the constituent type
                    constituent = elem.text

            if word_order > 0:
                words.append((word_id, word_order, constituent))

        sentences.append((sentence_id, words))

    return sentences


def parse_m_sentences(filename: str) -> [(str, [(str, str, str)])]:
    """
    Parses all sentences from one m-file and processes them to chosen format. This is a helper
    function for ``parse_sentences`` function. The chosen format is a list of sentences, where
    each sentence is a tuple of ID and a list of words, where each word is a triple containing
    the word ID, the actual word, and a string with tags.
    :param filename: name of XML file with morphologically annotated data
    :return: list of sentences in chosen format
    """
    # Initializing sentences list
    sentences = []

    # Initializing XML parser
    xml_m = ET.parse(resdir + r'\unpacked_m' + '\\' + filename + '.m')
    m_sentences = xml_m.findall('{http://ufal.mff.cuni.cz/pdt/pml/}s')

    for s in m_sentences:
        # ID starts with "m-", which is only an indicator of the morphological file,
        # we only want the ID itself
        sentence_id = s.get('id')[2:]

        # Initializing list of words in one sentence
        words = []
        for m in s:
            word_id = m.get('id').split('-')[3]
            actual_word, tag = None, None

            for elem in m:
                if re.match('.*form$', elem.tag):
                    # writing the actual word
                    actual_word = elem.text
                if re.match('.*tag$', elem.tag):
                    # writing word tag
                    tag = elem.text

            words.append((word_id, actual_word, tag))

        sentences.append((sentence_id, words))

    return sentences


def join_word_properties(words_a: [(str, int, str)], words_m: [(str, str, str)]) -> [(int, str, str, str)]:
    """
    Gets morphological and syntactical properties of words in one sentences and joins them
    together in one list of tuples.
    :param words_a: list of syntactical properties
    :param words_m: list of morphological properties
    :return: list of joined properties
    """
    # Initializing word list
    words = [(order, actual, tags, const)
             for id_a, order, const in words_a
             for id_m, actual, tags in words_m
             if id_a == id_m]

    words = sorted(words, key=lambda word: word[0])

    return words


def print_sentence(sentence: (str, [(int, str, str, str)]), file) -> None:
    """
    Prints one sentence in chosen format into output file.
    :param sentence: tuple of sentence ID and list of words
    :param file: output file
    :return: nothing
    """
    sentence_id, words = sentence
    f.write(sentence_id + '\n')
    for word in words:
        f.write(str(word[0]) + '\t' + word[1] + '\t' + word[2] + '\t' + word[3] + '\n')

    f.write('\n')


if __name__ == '__main__':
    resdir = get_pdt_folder()

    with open(resdir + r'\sentence_IDs_all.txt', mode='r', encoding='utf-8') as f:
        filenames = read_ids_from_file(f)

    for filename in filenames:
        sentences = parse_sentences(filename)

        with open(resdir + rf'\parsed_sentences\{filename}.txt', mode='w', encoding='utf-8') as f:
            for sentence in sentences:
                print_sentence(sentence, f)
