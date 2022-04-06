from src.rikli.sentence import load_sentences
from src.rikli.file import get_pdt_folder


if __name__ == '__main__':
    resdir = get_pdt_folder('parsed_sentences')

    with open(resdir + rf'\cmpr9406_001.txt', mode='r', encoding='utf-8') as f:
        sentences = load_sentences(f)

    print(sentences)
