import argparse
import json
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--data_to_examine',dest = 'data_to_examine',help = 'numerical summary of words in poetry corpus')
parser.add_argument('--word',dest = 'word',help = 'word that user wishes to know its percent overlap prewar and postwar')
args = parser.parse_args()

word_neighborhood_dictionary = {}
word_overlap_dictionary = {}
with gzip.open(args.data_to_examine,'r') as ifd:
    for line in ifd:
        my_dict = json.loads(line)
        (word,information), = my_dict.items()

        neighborhood = information['neighborhood spread']
        word_neighborhood_dictionary[word] = neighborhood

        percent_overlap = information['percent overlap prewar and postwar']
        word_overlap_dictionary[word] = percent_overlap

word_overlap = list(word_overlap_dictionary.items())
word_overlap_sorted = sorted(word_overlap,key = lambda any_word:any_word[1],reverse = True)
print(word_overlap_sorted)