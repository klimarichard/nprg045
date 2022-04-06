import typing


def read_ids_from_file(file: typing.TextIO) -> list[str]:
    """
    Reads list of sorted sentence IDs from a file containing one ID per line and
    parse the IDs to list of filenames.
    :param file: file with sentence IDs
    :return: list of filenames
    """
    return parse_filenames(read_ids(file))


def read_ids(file: typing.TextIO) -> list[str]:
    """
    Reads list of sorted sentence IDs from a file containing one ID per line.
    :param file: file with sentence IDs
    :return: list with read sentence IDs
    """
    ids = []

    for line in file:
        ids.append(line.strip())

    return ids


def parse_filenames(ids: list[str]) -> list[str]:
    """
    Gets list of filenames from list of sentence IDs.
    :param ids: list of sentence IDs
    :return: list of filenames
    """
    filenames = []
    old_filename = ''

    for sentence_id in ids:
        parsed_id = sentence_id.split('-')
        new_filename = parsed_id[0] + '_' + parsed_id[1]

        if new_filename != old_filename:
            old_filename = new_filename

            filenames.append(new_filename)

    return filenames


def get_pdt_folder(path: str = None) -> str:
    """
    Returns full path to ``/res/PDT/`` folder of the project.
    :param path: optional following path from PDT folder (use backward slash
                 as folder divider)
    :return: full path to ``/res/PDT/`` folder
    """
    import os

    if path:
        return os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT' + rf'\{path}'
    else:
        return os.path.sep.join(os.getcwd().split(os.path.sep)[:-2]) + r'\res\PDT'
