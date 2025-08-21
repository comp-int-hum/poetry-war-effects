import argparse
import json
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--data_to_examine',dest = 'data_to_examine',help = 'data extracted in extract_neighbors.py')
parser.add_argument('--topn_to_print',dest = 'topn_to_print',type = int,default = 10,help = 'the topn most similar words to show in the output')
parser.add_argument('--words_numerical_output',dest = 'words_numerical_output',help = 'dictionary containing neighborhood spread and percent overlap of words prewar and postwar')
parser.add_argument('--holistic_information',dest = 'holistic_information',help = 'dictionary containing the word, percent overlap of its neighbors prewar and postwar, its topn similar words prewar, and its topn similar words postwar')
args = parser.parse_args()

def spread(sims_prewar,sims_postwar):
    prewar_scores = []
    postwar_scores = []
    
    for top_word,score in sims_prewar:
        prewar_scores.append(score)
    prewar_neighborhood_cluster = max(prewar_scores) - min(prewar_scores)

    for top_word,score in sims_postwar:
        postwar_scores.append(score)
    postwar_neighborhood_cluster = max(postwar_scores) - min(postwar_scores)

    return {'prewar':prewar_neighborhood_cluster,'postwar':postwar_neighborhood_cluster}

def overlap(sims_prewar,sims_postwar):
    prewar_words = []
    postwar_words = []

    for top_word,score in sims_prewar:
        prewar_words.append(top_word)
    for top_word,score in sims_postwar:
        postwar_words.append(top_word)

    set_sims_prewar = set(prewar_words)
    set_sims_postwar = set(postwar_words)
    intersection = len(set_sims_prewar & set_sims_postwar)
    percent_overlap = intersection / len(sims_prewar)

    return percent_overlap

jsonl_data = {}
word_overlap_dictionary = {}
dict_to_print = {}
with gzip.open(args.data_to_examine,'r') as ifd,gzip.open(args.words_numerical_output,'wt') as ofd_num,gzip.open(args.holistic_information,'wt') as ofd_hol:
    for line in ifd:
        my_dict = json.loads(line)
        jsonl_data.update(my_dict)
        (word,information), = my_dict.items()
        sims_prewar = information['sims_prewar']
        sims_postwar = information['sims_postwar']
        neighborhood = spread(sims_prewar,sims_postwar)
        percent_overlap = overlap(sims_prewar,sims_postwar)
        word_dictionary = {
                word:{
                    'neighborhood spread':neighborhood,
                    'percent overlap prewar and postwar':percent_overlap
                }
            }
        ofd_num.write(json.dumps(word_dictionary)+ '\n')

        word_overlap_dictionary[word] = percent_overlap
    word_overlap = list(word_overlap_dictionary.items())
    ranking = sorted(word_overlap,key = lambda any_word:any_word[1],reverse = True)

    for word,score in ranking:
        prewar_words = []
        postwar_words = []
        prewar_information = jsonl_data[word]['sims_prewar']
        postwar_information = jsonl_data[word]['sims_postwar']
        for i,item in enumerate(prewar_information):
            if i > args.topn_to_print - 1:
                break
            else:
                prewar_words.append(item[0])

        for i,item in enumerate(postwar_information):
            if i > args.topn_to_print - 1:
                break
            else:
                postwar_words.append(item[0])

        dict_to_print = {
                word:{
                    'percent overlap':score,
                    'similar words prewar':prewar_words,
                    'similar words postwar':postwar_words
                }
            }
        ofd_hol.write(json.dumps(dict_to_print)+ '\n')
