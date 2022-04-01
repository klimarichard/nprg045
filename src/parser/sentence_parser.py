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


def parse_sentences(filename: str) -> [(str, [(int, str, str)])]:
    """
    Parses all sentences from one file and processes them to chosen format. The chosen format output
    is a list of sentences, where each sentence is a tuple of ID and a list of words, where each word
    is a triple containing word order in sentence, the actual word, and a string with tags.
    :param filename: name of XML file with annotated data
    :return: list of sentences in chosen format
    """
    # Initializing sentence list
    sentences = []

    # loading two corresponding XML files with syntactically and morphologically annotated data
    xml_a = ET.parse(resdir + r'\unpacked_a' + '\\' + filename + '.a')
    xml_m = ET.parse(resdir + r'\unpacked_m' + '\\' + filename + '.m')
    root_a = xml_a.getroot()
    root_m = xml_m.getroot()

    a_tree = xml_a.find('{http://ufal.mff.cuni.cz/pdt/pml/}trees')
    a_sentences = a_tree.findall('{http://ufal.mff.cuni.cz/pdt/pml/}')
    m_sentences = xml_m.findall('{http://ufal.mff.cuni.cz/pdt/pml/}s')

    for s in m_sentences:
        for m in s:
            # ID is a property of m tag, we need it to pair it with
            # the syntactical file
            word = [m.get('id').split('-')[3], -1, '', '']
            for elem in m:
                if re.match('.*form$', elem.tag):
                    word[2] = elem.text
                if re.match('.*tag$', elem.tag):
                    word[3] = elem.text

            print(word)

    return None


if __name__ == '__main__':
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT'

    with open(resdir + r'\sentence_IDs_all.txt', mode='r', encoding='utf-8') as f:
        IDs = read_ids(f)

    parse_sentences('cmpr9406_001')
