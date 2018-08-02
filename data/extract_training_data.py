#!/usr/bin/env python3
"""
Normalization:
    lowercase, one line = one sentence

all functions assumes dataset in memory for simplicity
"""
import argparse
import re
import string


def remove_empty_rows(text):
    return "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])


def remove_punctuations(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def lowercase(text):
    return text.lower()


def max_one_sentence_per_line(text):
    # https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
    caps = "([A-Z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    def split_into_sentences(text):
        text = " " + text + "  "
        text = text.replace("\n", " ")
        text = re.sub(prefixes, "\\1<prd>", text)
        text = re.sub(websites, "<prd>\\1", text)
        if "Ph.D" in text:
            text = text.replace("Ph.D.", "Ph<prd>D<prd>")
        text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
        text = re.sub(acronyms+" "+starters, "\\1<stop> \\2", text)
        text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
        text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
        text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
        text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
        text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
        if "”" in text:
            text = text.replace(".”", "”.")
        if "\"" in text:
            text = text.replace(".\"", "\".")
        if "!" in text:
            text = text.replace("!\"", "\"!")
        if "?" in text:
            text = text.replace("?\"", "\"?")
        text = text.replace(".", ".<stop>")
        text = text.replace("?", "?<stop>")
        text = text.replace("!", "!<stop>")
        text = text.replace("<prd>", ".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences

    return '\n'.join(split_into_sentences(text))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_dataset')
    parser.add_argument('norm_input')
    parser.add_argument('norm_output')
    args = parser.parse_args()

    with open(args.raw_dataset, 'r') as r, open(args.norm_input, 'w') as inp, open(args.norm_output, 'w') as outp:
        raw_text = r.read()
        one_sents = max_one_sentence_per_line(raw_text)
        norm_one_sents = lowercase(remove_punctuations(remove_empty_rows(one_sents)))
        inp.write(norm_one_sents)
        outp.write(norm_one_sents)
