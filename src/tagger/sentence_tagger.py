from src.rikli.sentence import load_sentences
from src.rikli.sentence import get_sentence
from src.rikli.file import get_pdt_folder
from src.tagger.phrase_searcher import phrase_search


def tag_sentence(sentence: tuple[str, list[tuple[int, str, str, str]]], tag_type: int = 0,
                 train_test: str = 'test') -> tuple[list[int], int]:
    """
    Tags sentence for comma completion task. It can produce many types of sentence tagging,
    depending on the second parameter. This function serves as a basis for building a data set
    of sentences for comma completion task.
    :param sentence: a sentence in chosen format
    :param tag_type: optional tag-type int,
                     0 (default) - sentence tagging based entirely on morphological tags
                     1           - sentence tagging based on morphological and syntactical tags (constituent type added)
    :param train_test: optional tag for determining whether this is a train set or test set,
                       'test' (default) - tag sentence without comma count, since it is unknown
                       'train'          - tag sentence with comma count for training the model
    :return: tuple of list of sentence tags and comma count
    """
    # Initializing return values
    comma_count = 0

    # Initializing helper values
    words = 0
    verbs = 0
    genitive = 0
    vocative = 0
    subordinate = 0
    non_subordinate = 0
    conj_that = 0  # že
    conj_sothat = 0  # aby
    conj_if = 0  # kdyby

    # Find first actual word (some example sentences start with a word with 'Z' word class)
    min_word = 0
    for word in sentence[1]:
        if word[2][0] != 'Z':
            min_word = word[0]
            break

    for word in sentence[1]:
        # If word is a comma, add to comma count
        if word[1] == ',':
            comma_count += 1
        # First tag is the word class, we only want words
        if word[2][0] != 'Z':
            words += 1
        # First tag says it is a verb, second tag says it is not on these three:
        #  c = conditional of the verb 'být'
        #  e = present transgressive
        #  f = infinitive
        #  m = past transgressive
        if word[2][0] == 'V' and word[2][1] not in 'cefm':
            verbs += 1
        # First tag says it is a noun
        if word[2][0] == 'N':
            # Fifth tag says it is in the second case
            if word[2][4] == '2':
                genitive += 1
            # Fifth tag says it is in the fifth case
            if word[2][4] == '5':
                vocative += 1
        # If the keywords are first in the sentence,
        # there cannot be a comma in front of them
        if word[0] > min_word:
            # If this word is a conjunction, look for keywords and subordinate and not subordinate conjunctions
            if word[2][0] == 'J':
                if word[1].lower() == 'že':
                    conj_that += 1
                if (word[1].lower() == 'aby' or word[1].lower() == 'abych' or word[1].lower() == 'abys' or
                        word[1].lower() == 'abychom' or word[1].lower() == 'abyste'):
                    conj_sothat += 1
                if (word[1].lower() == 'kdyby' or word[1].lower() == 'kdybych' or word[1].lower() == 'kdybys' or
                        word[1].lower() == 'kdybychom' or word[1].lower() == 'kdybyste'):
                    conj_if += 1
                # The second tag marks subordinate and not subordinate conjunctions
                if word[2][1] == ',':
                    subordinate += 1
                if word[2][1] == '^':
                    non_subordinate += 1

    # Find common phrases (we send all words but no punctuation
    common_phrases = phrase_search([(n, word) for (n, word, tags, _) in sentence[1] if tags[0] != 'Z'])

    tags = [words, verbs, genitive, vocative, common_phrases, subordinate, non_subordinate, conj_that,
            conj_sothat, conj_if]

    # Include tags based on constituent type
    if tag_type == 1:
        # Initialize helper values for constituent types
        adv, apos, atr, atv, atvv = 0, 0, 0, 0, 0,
        auxg, auxo, auxp, auxr, auxt, auxv, auxy = 0, 0, 0, 0, 0, 0, 0
        auxz, coord, obj, pnom, pred, sb = 0, 0, 0, 0, 0, 0

        for word in sentence[1]:
            if word[3] == 'Adv':
                adv += 1
            if word[3] == 'Apos':
                apos += 1
            if word[3] == 'Atr':
                atr += 1
            if word[3] == 'Atv':
                atv += 1
            if word[3] == 'AtvV':
                atvv += 1
            if word[3] == 'AuxG':
                auxg += 1
            if word[3] == 'AuxO':
                auxo += 1
            if word[3] == 'AuxP':
                auxp += 1
            if word[3] == 'AuxR':
                auxr += 1
            if word[3] == 'AuxT':
                auxt += 1
            if word[3] == 'AuxV':
                auxv += 1
            if word[3] == 'AuxY':
                auxy += 1
            if word[3] == 'AuxZ':
                auxz += 1
            if word[3] == 'Coord':
                coord += 1
            if word[3] == 'Obj':
                obj += 1
            if word[3] == 'Pnom':
                pnom += 1
            if word[3] == 'Pred':
                pred += 1
            if word[3] == 'Sb':
                sb += 1

        # Add constituent type values to tags
        tags += [adv, apos, atr, atv, atvv, auxg, auxo, auxp, auxr, auxt, auxv, auxy, auxz, coord, obj, pnom, pred, sb]

    if train_test == 'train':
        return tags, comma_count
    elif train_test == 'test':
        return tags, -1


if __name__ == '__main__':
    resdir = get_pdt_folder()

    for filename in ['comma', 'no_comma']:
        for const in ['', 'no_const_']:

            with open(resdir + rf'\parsed_sentences_commas\sentences_{filename}.txt', mode='r', encoding='utf-8') as f, \
                    open(resdir + rf'\tagged_sentences\tagged_{const}{filename}.txt', mode='w', encoding='utf-8') as g:
                sentences = load_sentences(f)

                for sentence in sentences:
                    if const == '':
                        g.write(sentence[0] + ': ' + str(tag_sentence(sentence, tag_type=1, train_test='train')) + '\n')
                    else:
                        g.write(sentence[0] + ': ' + str(tag_sentence(sentence, train_test='train')) + '\n')
