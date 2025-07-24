from gensim.models import Word2Vec
import argparse

import json
import gzip
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i1','--input_prewar',dest = 'input_prewar',help = 'prewar jsonlines file')
parser.add_argument('-i2','--input_postwar',dest = 'input_postwar',help = 'postwar jsonlines file')
parser.add_argument('-o1','--output_prewar',dest = 'output_prewar',help = 'prewar model')
parser.add_argument('-o2','--output_postwar',dest = 'output_postwar',help = 'postwar model')
parser.add_argument('-o3','--prewar_vocab',dest = 'prewar_vocab',help = 'dictionary of all words used to train prewar model')
parser.add_argument('-o4','--postwar_vocab',dest = 'postwar_vocab',help = 'dictionary of all words used to train postwar model')
args = parser.parse_args()

word_list_prewar = []
word_list_postwar = []

with gzip.open(args.input_prewar,'r') as ifd_prewar:
    for line_prewar in ifd_prewar:
        poem_prewar = json.loads(line_prewar)
        content_prewar = poem_prewar['content']['stanzas']
        for stanza_prewar in content_prewar:
            for unprocessed_sentence_prewar in stanza_prewar:
                initial_processed_sentence_prewar = unprocessed_sentence_prewar.rstrip('\n').lower()
                sentence_prewar = re.sub(r'[^\w\s]', '', initial_processed_sentence_prewar)
                word_list_per_sentence_prewar = sentence_prewar.split(' ')
                word_list_prewar.append(word_list_per_sentence_prewar)

dict_prewar = {}
for line in word_list_prewar:
    for word in line:
        if word not in dict_prewar:
            dict_prewar[word] = 1
        else:
            dict_prewar[word] += 1
with open(args.prewar_vocab,'w') as ifd_prewar_wordcount:
    json.dump(dict_prewar,ifd_prewar_wordcount)

with gzip.open(args.input_postwar,'r') as ifd_postwar:
    for line_postwar in ifd_postwar:
        poem_postwar = json.loads(line_postwar)
        content_postwar = poem_postwar['content']['stanzas']
        for stanza_postwar in content_postwar:
            for unprocessed_sentence_postwar in stanza_postwar:
                initial_processed_sentence_postwar = unprocessed_sentence_postwar.rstrip('\n').lower()
                sentence_postwar = re.sub(r'[^\w\s]', '', initial_processed_sentence_postwar)
                word_list_per_sentence_postwar = sentence_postwar.split(' ')
                word_list_postwar.append(word_list_per_sentence_postwar)
dict_postwar = {}
for line in word_list_postwar:
    for word in line:
        if word not in dict_postwar:
            dict_postwar[word] = 1
        else:
            dict_postwar[word] += 1
with open(args.postwar_vocab,'w') as ifd_postwar_wordcount:
    json.dump(dict_postwar,ifd_postwar_wordcount)

model_prewar = Word2Vec(sentences = word_list_prewar, vector_size = 100, window = 5, min_count = 1, workers = 4)
model_prewar.save(args.output_prewar)
model_postwar = Word2Vec(sentences = word_list_postwar, vector_size = 100, window = 5, min_count = 1, workers = 4)
model_postwar.save(args.output_postwar)
