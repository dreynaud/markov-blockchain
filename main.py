# -*- coding: utf-8 -*-

from collections import defaultdict

import os
import random
import re
import sys

# from https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
def split_into_sentences(text):
    caps = "([A-Z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"

    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

class Markov(object):
    START = 'START'
    END = 'END'

    def __init__(self):
        super(Markov, self).__init__()
        self.chain = defaultdict(list)

    def train(self, sentence):
        words = sentence.lower().split()
        curr_token = Markov.START
        for word in words:
            if word[-1] == '.':
                stripped_word = word[:-1]
                self.chain[curr_token].append(stripped_word)
                self.chain[stripped_word].append(Markov.END)

                if word != words[-1]:
                    print 'WARNING: break in middle of sentence:', words

                break

            self.chain[curr_token].append(word)
            curr_token = word

    def generate(self):
        curr_token = Markov.START
        words = []
        while curr_token != Markov.END:
            next_word = random.choice(self.chain[curr_token])
            words.append(next_word)
            curr_token = next_word

        return ' '.join(words[:-1]) # strip the END token

    def __repr__(self):
        return repr(self.chain)


def main():
    markov = Markov()
    for f in os.listdir('corpus'):
        with open(os.path.join('corpus', f)) as fd:
            text = fd.read()
            sentences = split_into_sentences(text)
            for sentence in sentences:
                markov.train(sentence)

    # print markov

    for i in xrange(int(sys.argv[1])):
        print markov.generate()

if __name__ == '__main__':
    main()