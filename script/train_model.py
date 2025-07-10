from gensim.models import Word2Vec
import argparse

import json
import gzip
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i',dest = 'input')
parser.add_argument('-o',dest = 'output')
args = parser.parse_args()

word_list = []
with gzip.open(args.input,'r') as ifd:
    for line in ifd:
        poem = json.loads(line)
        content = poem['content']['stanzas']
        for stanza in content:
            for unprocessed_sentence in stanza:
                initial_processed_sentence = unprocessed_sentence.rstrip('\n').lower()
                sentence = re.sub(r'[^\w\s]', '', initial_processed_sentence)
                word_list_per_sentence = sentence.split(' ')
                word_list.append(word_list_per_sentence)

model = Word2Vec(sentences = word_list, vector_size = 100, window = 5, min_count = 1, workers = 4)
model.save("work/word2vec.model")