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

            # Last string contains a new line at the end, hence the strip call
            words.append((int(line_split[0]), line_split[1], line_split[2], line_split[3].strip()))
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
            sentences.append((sentence_id.strip(), words))

            # Restore default values
            words = []
            new_sentence = True
            comma = False

    return sentences


def get_sentence(sentence: tuple[str, list[tuple[int, str, str, str]]]) -> str:
    """
    Finds the actual sentence for printing.
    :param sentence: tuple of sentence ID and list of words
    :return: string with the actual sentence
    """
    final_sentence = ''

    if len(sentence[1]) > 0:
        final_sentence += sentence[1][0][1]

    # Indicator for some chars, e.g. '(', that there should not be a space after
    if sentence[1][0][1] == '(':
        no_space = True
    else:
        no_space = False

    if len(sentence[1]) > 1:
        for i in range(1, len(sentence[1])):
            if ((not no_space) and
                    (sentence[1][i][2][0] != 'Z' or
                        (sentence[1][i][2][0] == 'Z' and
                            sentence[1][i][1] in '(-'))):
                final_sentence += ' '

            final_sentence += sentence[1][i][1]

            if sentence[1][i][1] == '(':
                no_space = True
            else:
                no_space = False

    return final_sentence


def find_all_constituent_types(sentences: list[tuple[str, list[tuple[int, str, str, str]]]],
                               filename: str = None) -> list[str]:
    """
    Finds all different constituent types in given list of sentences.
    :param sentences: list of sentences in chosen format
    :param filename: optional name of output file to write constituent types to
    :return: list of constituent types
    """
    # Initializing return list
    constituents = []

    # Look through all sentences and find constituent types
    for sentence in sentences:
        for word in sentence[1]:
            if word[3] not in constituents:
                constituents.append(word[3])

    # Sort list of constituent types
    constituents = sorted(constituents)

    if filename:
        with open(filename, mode='w', encoding='utf-8') as f:
            for i in range(len(constituents)):
                f.write(constituents[i])
                if i < len(constituents) - 1:
                    f.write(', ')

    return constituents
