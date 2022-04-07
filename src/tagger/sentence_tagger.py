from src.rikli.sentence import load_sentences
from src.rikli.sentence import get_sentence
from src.rikli.file import get_pdt_folder


def tag_sentence(sentence: tuple[str, list[tuple[int, str, str, str]]], tag_type: int = 0) -> tuple[list[int], int]:
    """
    Tags sentence for comma completion task. It can produce many types of sentence tagging,
    depending on the second parameter. This function serves as a basis for building a data set
    of sentences for comma completion task.
    :param sentence: a sentence in chosen format
    :param tag_type: optional tag-type int,
                     0 (default) - sentence tagging based entirely on morphological tags
                     1           - sentence tagging based on morphological and syntactical tags (constituent type added)
    :return: tuple of list of sentence tags and comma count
    """
    # Initializing return values
    tags = []
    comma_count = 0

    # Initializing helper values
    word_count = 0
    verb_count = 0

    for word in sentence[1]:
        # If word is a comma, add to comma count
        if word[1] == ',':
            comma_count += 1
        # First tag is the word class, we only want words
        if word[2][0] != 'Z':
            word_count += 1
        # First tag says it is a verb, second tag says it is not on these three:
        #  e = present transgressive
        #  f = infinitive
        #  m = past transgressive
        if word[2][0] == 'V' and word[2][1] not in 'efm':
            verb_count += 1

    tags = [word_count, verb_count]

    return tags, comma_count


if __name__ == '__main__':
    resdir = get_pdt_folder('parsed_sentences')

    with open(resdir + rf'\ln94200_3.txt', mode='r', encoding='utf-8') as f:
        sentences = load_sentences(f)

    for sentence in sentences:
        print(get_sentence(sentence) + '\t', tag_sentence(sentence))
