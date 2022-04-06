import typing


def write_sentence_to_file(file: typing.TextIO, sentence_id: str, words: list[tuple[int, str, str, str]]) -> None:
    """
    Writes given sentence to output file.
    :param file: output file
    :param sentence_id: ID of the sentence
    :param words: list of words in the sentence
    :return: nothing
    """
    file.write(sentence_id)

    for word in words:
        file.write(str(word[0]) + '\t' + word[1] + '\t' + word[2] + '\t' + word[3] + '\n')

    file.write('\n')


def load_sentences(f: typing.TextIO, file_no_comma: typing.TextIO = None,
                   file_comma: typing.TextIO = None) -> list[tuple[str, list[tuple[int, str, str, str]]]]:
    """
    Loads sentences from one file with parsed sentences and determine, if they contain a comma.
    Then write the sentences to ``sentences_no_comma.txt`` and ``sentences_comma.txt``
    respectively, if those files are provided.
    :param f: input file with parsed sentences
    :param file_no_comma: optional output file for sentences with no commas
    :param file_comma: optional output file for sentences with commas
    :return: list of sentences in chosen format
    """
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
        file2 = False

    for line in f:
        # Start of a new sentence (sentence ID)
        if new_sentence:
            sentence_id = line
            new_sentence = False
        # Read words in sentence
        elif line != '\n':
            line_split = line.split('\t')

            # If the word is a comma, mark the sentence as one with commas
            if line_split[1] == ',':
                comma = True

            words.append((int(line_split[0]), line_split[1], line_split[2], line_split[3]))
        # Empty line denotes the end of the sentence
        else:
            # If there are more new lines in sequence
            if len(words) == 0:
                continue

            # If file for no comma sentences was provided
            if file1:
                write_sentence_to_file(file_no_comma, sentence_id, words)

            # If file for comma sentences was provided and the sentence contained a comma
            if file2 & comma:
                write_sentence_to_file(file_comma, sentence_id, words)

            # Append sentence to return list
            sentences.append((sentence_id, words))

            # Restore default values
            words = []
            new_sentence = True
            comma = False

    return sentences
