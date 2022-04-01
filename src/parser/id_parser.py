import os
import re
import xml.etree.ElementTree as ET

from functools import cmp_to_key


def parse_m_file(filename: str) -> [str]:
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


def parse_a_file(filename: str) -> [str]:
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


def set_final_ID_list(longer_list: [str], shorter_list: [str]) -> [str]:
    """
    Sets the final ID list from the two lists given.
    :param longer_list: longer of the two lists
    :param shorter_list: shorter of the two lists
    :return: final ID list if found, or
             None if there are some IDs present in the shorter list not present in the longer list
    """
    # verify that no IDs present in the shorter are missing from the longer list
    if len(set(shorter_list).difference(longer_list)) == 0:
        print('All IDs present in the longer list.')

        # sets final ID list as the shorter list
        return sort_id_list(shorter_list)
    else:
        print('Some IDs present in the shorter list are missing from the longer list:')

        # Print the IDs missing from the longer list and exit program.
        print(sort_id_list(list(set(shorter_list).difference(longer_list))))
        return None


def sort_id_list(ids: [str]) -> [str]:
    """
    Sorts list of IDs for simpler file reading.
    :param ids: list of IDs
    :return: nothing
    """
    ids.sort(key=cmp_to_key(compare_ids))

    return ids


def compare_ids(id1: str, id2: str) -> int:
    """
    Compares two ID values.
    :param id1: first ID value
    :param id2: second ID value
    :return:  1, if the first value is greater than the second one,
              0, if they are the same,
             -1, if the first value is lesser than the second one
    """
    # split ID into three segments
    # ID is of xxxxNNN-NNN-xNNxNN type
    split1 = id1.split('-')
    split2 = id2.split('-')

    # letter part of first segment
    first1 = ''.join([x for x in split1[0] if not x.isdigit()])
    first2 = ''.join([x for x in split2[0] if not x.isdigit()])

    # number part of first segment
    second1 = int(''.join([x for x in split1[0] if x.isdigit()]))
    second2 = int(''.join([x for x in split2[0] if x.isdigit()]))

    # number from the second segment
    third1 = split1[1]
    third2 = split2[1]

    # first number from the third segment
    fourth1 = int(''.join([x for x in split1[2].split('s')[0] if x.isdigit()]))
    fourth2 = int(''.join([x for x in split2[2].split('s')[0] if x.isdigit()]))

    # second number from the third segment
    fifth1 = int(''.join([x for x in split1[2].split('s')[1] if x.isdigit()]))
    fifth2 = int(''.join([x for x in split2[2].split('s')[1] if x.isdigit()]))

    # compare the segments one by one (only if all segments are equal are the IDs equal)
    if first1 > first2:
        return 1
    elif first1 < first2:
        return -1
    else:
        if second1 > second2:
            return 1
        elif second1 < second2:
            return -1
        else:
            if third1 > third2:
                return 1
            if third1 < third2:
                return -1
            else:
                if fourth1 > fourth2:
                    return 1
                if fourth1 < fourth2:
                    return -1
                else:
                    if fifth1 > fifth2:
                        return 1
                    if fifth1 < fifth2:
                        return -1
                    else:
                        return 0


if __name__ == '__main__':
    # Initializing lists of IDs for morphologically and syntactically annotated files
    all_m_IDs = []
    all_a_IDs = []

    # Initializing final ID list
    final_ID_list = []

    # Find all morphologically annotated files and parse their sentence IDs
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\unpacked_m'
    for f in os.listdir(resdir):
        all_m_IDs += (parse_m_file(os.path.join(resdir, f)))

    print('Morphologically annotated files successfully loaded.')

    # Find all syntactically annotated files and parse their sentence IDs
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\unpacked_a'
    for f in os.listdir(resdir):
        all_a_IDs += (parse_a_file(os.path.join(resdir, f)))

    print('Syntactically annotated files successfully loaded.')

    print('---------------')

    if len(all_a_IDs) == len(all_m_IDs):
        print('Both ID lists have the same length.')
        print('The length of the lists is ' + str(len(all_m_IDs)))

        # Verify that no IDs present in one list are missing from the other and vice versa
        if len(set(all_a_IDs).difference(all_m_IDs)) == 0 and len(set(all_m_IDs).difference(all_a_IDs)) == 0:
            print('Both lists contain the same IDs.')

            # Sets final ID list as either of the two lists (e.g. morphological)
            final_ID_list = sort_id_list(all_m_IDs)
        else:
            print('There are some IDs present in one list that are not in the other.')
    if len(all_a_IDs) < len(all_m_IDs):
        print('The morphological ID list is longer than the syntactical ID list.')
        print('The length of the morphological list is ' + str(len(all_m_IDs)) + '.')
        print('The length of the syntactical list is ' + str(len(all_a_IDs)) + '.')

        final_ID_list = set_final_ID_list(all_m_IDs, all_a_IDs)
    else:
        print('The syntactical ID list is longer than the morphological ID list.')
        print('The length of the syntactical list is ' + str(len(all_a_IDs)) + '.')
        print('The length of the morphological list is ' + str(len(all_m_IDs)) + '.')

        final_ID_list = set_final_ID_list(all_a_IDs, all_m_IDs)

    if final_ID_list:
        print('---------------')
        print('Final ID list found.')

        resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT'

        with open(resdir + r'\sentence_IDs_all.txt', mode='w', encoding='utf-8') as f:
            for i in range(len(final_ID_list)):
                f.write(final_ID_list[i])
                if i != len(final_ID_list) - 1:
                    f.write('\n')

        print('Final ID list successfully written to file ' + resdir + r'\sentence_IDs_all.txt.')
    else:
        print('There were no final IDs found (probably because there were some IDs present in the shorter list, that ' +
              'were not present in the longer list).')
        exit(1)
