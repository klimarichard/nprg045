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
    words = 0
    verbs = 0
    vocative = 0
    conj_that = 0 # že
    conj_sothat = 0 # aby
    conj_if = 0 # kdyby

    for word in sentence[1]:
        # If word is a comma, add to comma count
        if word[1] == ',':
            comma_count += 1
        # First tag is the word class, we only want words
        if word[2][0] != 'Z':
            words += 1
        # First tag says it is a verb, second tag says it is not on these three:
        #  e = present transgressive
        #  f = infinitive
        #  m = past transgressive
        if word[2][0] == 'V' and word[2][1] not in 'efm':
            verbs += 1
        # First tag says it is a noun, fifth tag says it is in the fifth case
        if word[2][0] == 'N' and word[2][4] == '5':
            vocative += 1
        if word[2][0] == 'J' and word[1].lower() == 'že':
            conj_that += 1
        if word[2][0] == 'J' and word[1].lower() == 'aby':
            conj_sothat += 1
        if word[2][0] == 'J' and word[1].lower() == 'kdyby':
            conj_if += 1

    tags = [words, verbs, vocative, conj_that, conj_sothat, conj_if]

    # Include tags based on constituent type
    if tag_type == 1:
        # Initialize helper values for constituent types
        adv, advatr, apos, atr, atradv, atratr, atrobj, atv, atvv = 0, 0, 0, 0, 0, 0, 0, 0, 0
        auxc, auxg, auxk, auxo, auxp, auxr, auxt, auxv, auxx, auxy = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        auxz, coord, exd, obj, objatr, pnom, pred, sb = 0, 0, 0, 0, 0, 0, 0, 0

        for word in sentence[1]:
            if word[3] == 'Adv':
                adv += 1
            if word[3] == 'AdvAtr':
                advatr += 1
            if word[3] == 'Apos':
                apos += 1
            if word[3] == 'Atr':
                atr += 1
            if word[3] == 'AtrAdv':
                atradv += 1
            if word[3] == 'AtrAtr':
                atratr += 1
            if word[3] == 'AtrObj':
                atrobj += 1
            if word[3] == 'Atv':
                atv += 1
            if word[3] == 'AtvV':
                atvv += 1
            if word[3] == 'AuxC':
                auxc += 1
            if word[3] == 'AuxG':
                auxg += 1
            if word[3] == 'AuxK':
                auxk += 1
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
            if word[3] == 'AuxX':
                auxx += 1
            if word[3] == 'AuxY':
                auxy += 1
            if word[3] == 'AuxZ':
                auxz += 1
            if word[3] == 'Coord':
                coord += 1
            if word[3] == 'ExD':
                exd += 1
            if word[3] == 'Obj':
                obj += 1
            if word[3] == 'ObjAtr':
                objatr += 1
            if word[3] == 'Pnom':
                pnom += 1
            if word[3] == 'Pred':
                pred += 1
            if word[3] == 'Sb':
                sb += 1

        # Add constituent type values to tags
        tags += [adv, advatr, apos, atr, atradv, atratr, atrobj, atv, atvv, auxc, auxg, auxk, auxo, auxp, auxr, auxt,
                 auxv, auxx, auxy, auxz, coord, exd, obj, objatr, pnom, pred, sb]

    return tags, comma_count


if __name__ == '__main__':
    resdir = get_pdt_folder('parsed_sentences')

    with open(resdir + rf'\ln94200_3.txt', mode='r', encoding='utf-8') as f:
        sentences = load_sentences(f)

    for sentence in sentences:
        print(get_sentence(sentence) + '\t', tag_sentence(sentence))
