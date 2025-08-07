import argparse
import json
import gzip
import re

parser = argparse.ArgumentParser()
# to add
# take a jsonlines file generated in data_extraction.py as parser argument
parser.add_argument('--output_wordcount',dest = 'output_wordcount',help = 'json file of wordcount dictionary')
args = parser.parse_args()

word_list = []

# to clean
# redo regular expressions
with gzip.open(args.input_data,'r') as ifd:
    for line in ifd:
        poem = json.loads(line)
        content = poem['content']['stanzas']
        for stanza in content:
            for unprocessed_sentence in stanza:
                initial_processed_sentence = unprocessed_sentence.rstrip('\n').lower()
                sentence = re.sub(r'[^\w\s]', '', initial_processed_sentence)
                word_list_per_sentence = sentence.split(' ')
                word_list.append(word_list_per_sentence)

dict_wordcount = {}
for line in word_list:
    for word in line:
        if word not in dict_wordcount:
            dict_wordcount[word] = 1
        else:
            dict_wordcount[word] += 1

# to add
# write word_list to a json file as well
with open(args.output_wordcount,'w') as ifd_wordcount:
    json.dump(dict_wordcount,ifd_wordcount)