# TODO: move relevant parts of code here for recycling
import typing


def write_sentence_to_file(file: typing.TextIO, sentence_id: str, words: [str]) -> None:
    """
    Writes given sentence to output file.
    :param file: output file
    :param sentence_id: ID of the sentence
    :param words: list of words in the sentence
    :return: nothing
    """
    file.write(sentence_id)

    for word in words:
        file.write(word)

    file.write('\n')
