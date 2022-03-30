import os
import re
import xml.etree.ElementTree as ET


def parse_m_file(filename) -> [str]:
    """
    Gets list of sentence IDs from given XML file of morphologically
    annotated data.
    :param filename: name of XML file with morphologically annotated data
    :return: list of found sentence IDs
    """
    IDs = []
    xml = ET.parse(filename)
    root = xml.getroot()

    for elem in root:
        # Filter only sentence tags
        if re.match(r'{.*}s', elem.tag):
            # The prefix 'm-' is not needed, it is and indicator
            # of the morphological file
            IDs.append(elem.attrib.get('id')[2:])

    return IDs


def parse_a_file(filename) -> [str]:
    """
    Gets list of sentence IDs from given XML file of syntactically
    annotated data.
    :param filename: name of XML file with syntactically annotated data
    :return: list of found sentence IDs
    """
    IDs = []
    xml = ET.parse(filename)
    root = xml.getroot()
    trees = root.find('{http://ufal.mff.cuni.cz/pdt/pml/}trees')

    for elem in trees:
        # Filter only sentence tags
        if re.match(r'.*{.*}LM', elem.tag):
            # The prefix 'a-' is not needed, it is and indicator
            # of the syntactical file
            IDs.append(elem.attrib.get('id')[2:])

    return IDs


if __name__ == '__main__':
    # Initializing lists of IDs for morphologically and syntactically annotated files
    all_m_IDs = []
    all_a_IDs = []

    # Find all morphologically annotated files and parse their sentence IDs
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\unpacked_m'
    for filename in os.listdir(resdir):
        all_m_IDs += (parse_m_file(os.path.join(resdir, filename)))

    # Find all syntactically annotated files and parse their sentence IDs
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\unpacked_a'
    for filename in os.listdir(resdir):
        all_a_IDs += (parse_a_file(os.path.join(resdir, filename)))

    print(all_a_IDs[0])
    print(all_m_IDs[0])
