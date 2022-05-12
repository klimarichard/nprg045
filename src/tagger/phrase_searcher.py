def phrase_search(sentence: tuple[str, list[tuple[int, str, str, str]]]) -> int:
    """
    Searches given sentence for known phrases containing a comma
    and returns number of commas that should be added to expected comma count.
    :param sentence: a sentence in chosen format
    :return: number of commas to be added to expected comma count
    """
