import typing


def write_sentence_to_file(file: typing.TextIO, sentence_id: str, words: list[str]) -> None:
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


def load_sentences(f: typing.TextIO, file_no_comma: typing.TextIO = None,
                   file_comma: typing.TextIO = None) -> list[tuple[str, list[tuple[int, str, str, str]]]]:
    # Initialize sentences list
    sentences = []

    # Initialize default values
    sentence_id = ''
    words = []
    new_sentence = True
    comma = False

    if file_no_comma:
        file1 = True
    else:
        file1 = False

    if file_comma:
        file2 = True
    else:
        file1 = False

    for line in f:
        # Start of a new sentence (sentence ID)
        if new_sentence:
            sentence_id = line
            new_sentence = False
        # Read words in sentence
        elif line != '\n':
            # If the word is a comma, mark the sentence as one with commas
            if line.split('\t')[1] == ',':
                comma = True
            words.append(line)
        # Empty line denotes the end of the sentence
        else:
            # If there are more new lines in sequence
            if len(words) == 0:
                continue

            # If there was a comma in the sentence
            if comma:
                write_sentence_to_file(file_comma, sentence_id, words)
            else:
                write_sentence_to_file(file_no_comma, sentence_id, words)

            # Restore default values
            words = []
            new_sentence = True
            comma = False

    return sentences
