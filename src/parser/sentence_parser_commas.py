import os


from sentence_parser import read_ids_from_file


def load_sentences_to_comma_files(filename: str, file_no_comma, file_comma) -> None:
    """
    Load sentences from one file with parsed sentences and determine, if they contain a comma.
    Then write the sentences to ``sentences_no_comma.txt`` and ``sentences_comma.txt``
    respectively.
    :param filename: name of a file with parsed sentences
    :param file_no_comma: output file for sentences with no commas
    :param file_comma: output file for sentences with commas
    :return: nothing
    """
    src_dir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\parsed_sentences'

    with open(src_dir + rf'\{filename}.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()

        # Initialize default values
        i = 0
        sentence_id = ''
        words = []
        new_sentence = True
        comma = False

        while i < len(lines):
            # Start of a new sentence (sentence ID)
            if new_sentence:
                sentence_id = lines[i]
                new_sentence = False
            # Read words in sentence
            elif lines[i] != '\n':
                # If the word is a comma, mark the sentence as one with commas
                if lines[i].split('\t')[1] == ',':
                    comma = True
                words.append(lines[i])
            # Empty line denotes the end of the sentence
            else:
                # If there are more new lines in sequence
                if len(words) == 0:
                    i += 1
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

            i += 1


def write_sentence_to_file(file, sentence_id: str, words: [str]) -> None:
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


if __name__ == '__main__':
    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT'

    with open(resdir + r'\sentence_IDs_all.txt', mode='r', encoding='utf-8') as f:
        filenames = read_ids_from_file(f)

    resdir = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT\parsed_sentences_commas'

    with open(resdir + r'\sentences_no_comma.txt', mode='w', encoding='utf-8') as file_no_comma, \
            open(resdir + r'\sentences_comma.txt', mode='w', encoding='utf-8') as file_comma:
        for filename in filenames:
            load_sentences_to_comma_files(filename, file_no_comma, file_comma)