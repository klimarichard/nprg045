def phrase_search(words: list[tuple[int, str]]) -> int:
    """
    Searches given sentence for known phrases containing a comma
    and returns number of commas that should be added to expected comma count.
    :param words: a list of tuples of word order in sentence and a word
    :return: number of commas to be added to expected comma count
    """
    words_only = [word for (_, word) in sorted(words)]

    phrases = two_conjunctions(words_only)

    return phrases


def two_conjunctions(words: list[str]) -> int:
    """
    Searches for instances of two conjunctions in a row, e.g.
    "že když", "protože když", "že kdyby", etc.
    :param words: list of words
    :return: number of instances of two conjunctions in a row
    """
    instances = 0

    # We don't care about the first word (no comma in front of it),
    # and the last word (no another word after it, so no two conjunctions in a row),
    # so the range is from the 2nd word to the second to last.
    for i in range(1, len(words) - 2):
        if words[i].lower() == 'že':
            if words[i + 1].lower() in ['když', 'kdyby', 'kdybych', 'kdybys', 'kdybychom', 'kdybyste', 'přestože']:
                instances += 1
        if words[i].lower() in ['protože', 'přestože']:
            if words[i + 1].lower() in ['když', 'kdyby', 'kdybych', 'kdybys', 'kdybychom', 'kdybyste']:
                instances += 1

    return instances
