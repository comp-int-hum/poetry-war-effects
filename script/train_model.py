from gensim.models import Word2Vec
import argparse
import json
import gzip
import re

parser = argparse.ArgumentParser()
parser.add_argument('--input_data',dest = 'input_data',help = 'zipped jsonlines file that the code takes in')
parser.add_argument('--output_wordcount',dest = 'output_wordcount',help = 'json file of wordcount dictionary')
parser.add_argument('--output_model',dest = 'output_model',help = 'trained Word2Vec model')
args = parser.parse_args()

word_list = []
with gzip.open(args.input_data,'r') as ifd:
    for line in ifd:
        poem = json.loads(line)
        content = poem['content']['stanzas']
        for stanza in content:
            for unprocessed_sentence in stanza:
                initial_processed_sentence = unprocessed_sentence.rstrip('\n').lower()
                step_one = re.sub(r'indent;',' ',initial_processed_sentence)
                step_two = re.sub(r"'",'',step_one)
                final_step = re.sub(r'[^a-z]',' ',step_two)
                word_list_per_sentence = final_step.split()
                word_list.append(word_list_per_sentence)

dict_wordcount = {}
for line in word_list:
    for word in line:
        if word not in dict_wordcount:
            dict_wordcount[word] = 1
        else:
            dict_wordcount[word] += 1

with open(args.output_wordcount,'w') as ifd_wordcount:
    json.dump(dict_wordcount,ifd_wordcount)

model = Word2Vec(sentences = word_list, vector_size = 100, window = 5, min_count = 1, workers = 4)
model.save(args.output_model)