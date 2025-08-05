import argparse
import json
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--data_to_examine',dest = 'data_to_examine',help = 'data extracted in extract_neighbors.py')
parser.add_argument('--words_numerical_output',dest = 'words_numerical_output',help = 'dictionary containing neighborhood spread and percent overlap of words prewar and postwar')
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

with gzip.open(args.data_to_examine,'r') as ifd,gzip.open(args.words_numerical_output,'wt') as ofd:
    for line in ifd:
        my_dict = json.loads(line)
        (word,information), = my_dict.items()
        sims_prewar = information['sims_prewar']
        sims_postwar = information['sims_postwar']
        word_dictionary = {
                word:{
                    'neighborhood spread':spread(sims_prewar,sims_postwar),
                    'percent overlap prewar and postwar':overlap(sims_prewar,sims_postwar)
                }
            }
        ofd.write(json.dumps(word_dictionary)+ '\n')