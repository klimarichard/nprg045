import typing

from src.rikli.file import read_ids_from_file
from src.rikli.file import get_pdt_folder
from src.rikli.sentence import load_sentences


def load_sentences_to_comma_files(filename: str, file_no_comma: typing.TextIO, file_comma: typing.TextIO) -> None:
    """
    Load sentences from one file with parsed sentences and determine, if they contain a comma.
    Then write the sentences to ``sentences_no_comma.txt`` and ``sentences_comma.txt``
    respectively.
    :param filename: name of a file with parsed sentences
    :param file_no_comma: output file for sentences with no commas
    :param file_comma: output file for sentences with commas
    :return: nothing
    """
    src_dir = get_pdt_folder('parsed_sentences')

    with open(src_dir + rf'\{filename}.txt', mode='r', encoding='utf-8') as f:
        load_sentences(f, file_no_comma, file_comma)


if __name__ == '__main__':
    resdir = get_pdt_folder()

    with open(resdir + r'\sentence_IDs_all.txt', mode='r', encoding='utf-8') as f:
        filenames = read_ids_from_file(f)

    resdir += r'\parsed_sentences_commas'

    with open(resdir + r'\sentences_no_comma.txt', mode='w', encoding='utf-8') as file_no_comma, \
            open(resdir + r'\sentences_comma.txt', mode='w', encoding='utf-8') as file_comma:
        for filename in filenames:
            load_sentences_to_comma_files(filename, file_no_comma, file_comma)
