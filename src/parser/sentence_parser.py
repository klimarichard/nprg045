import os
import re
import xml.etree.ElementTree as ET


def read_ids(file) -> [str]:
    """
    Reads list of sorted sentence IDs from a file containing one ID per line.
    :param file: file with sentence IDs
    :return: list with read sentence IDs
    """
    IDs = []

    for line in file:
        IDs.append(line.strip())

    return IDs


def parse_sentences(filename: str) -> [(str, [(int, str, str, str)])]:
    """
    Parses all sentences from corresponding m- and a-files and processes them to chosen format.
    The chosen format is a list of sentences, where each sentence is a tuple of ID and a list of words,
    where each word is a quadruple containing word order in sentence, the actual word, constituent type,
    and a string with tags.
    :param filename: name of XML files (without extension) with annotated data
    :return: list of sentences in chosen format
    """
    # Initializing sentence lists
    sentences = []
    sentences_m = parse_m_sentences(filename)
    sentences_a = parse_a_sentences(filename)

    # TODO: incorporate syntactically annotated data
    # TODO: join data from two different types of files
    # TODO: return sentences in chosen format

    return None


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
    a_lms = xml_a.iter('{http://ufal.mff.cuni.cz/pdt/pml/}LM')

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
    root_m = xml_m.getroot()
    m_sentences = xml_m.findall('{http://ufal.mff.cuni.cz/pdt/pml/}s')

    for s in m_sentences:
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


if __name__ == '__main__':
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT'

    with open(resdir + r'\sentence_IDs_all.txt', mode='r', encoding='utf-8') as f:
        IDs = read_ids(f)
