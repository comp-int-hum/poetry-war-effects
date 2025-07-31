from gensim.models import Word2Vec
import argparse
import json
import gzip

parser = argparse.ArgumentParser()
parser.add_argument('--prewar_model',dest = 'prewar_model',help = 'trained prewar model')
parser.add_argument('--postwar_model',dest = 'postwar_model',help = 'trained postwar model')
parser.add_argument('--prewar_wordcount',dest = 'prewar_wordcount',help = 'dictionary of words used in prewar poetry')
parser.add_argument('--postwar_wordcount',dest = 'postwar_wordcount',help = 'dictionary of words used in postwar poetry')
parser.add_argument('--topn_words',dest = 'topn_words',type = int, default = 10, help = 'top n similar words to examine')
parser.add_argument('--min_word_count',dest = 'min_word_count',type = int,default = 10, help = 'number of times a word must appear in word count dictionary to be evaluated')
parser.add_argument('--output',dest = 'output',help = 'output of the script')
args = parser.parse_args()

model_prewar = Word2Vec.load(args.prewar_model)
model_postwar = Word2Vec.load(args.postwar_model)

def extraction(model1,model2,word,topn):
    sims_prewar = model1.wv.most_similar(word,topn = topn)
    sims_postwar = model2.wv.most_similar(word,topn = topn)
    return sims_prewar,sims_postwar

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



with open(args.prewar_wordcount,'r') as ifd_prewar:
    dict_prewar = json.load(ifd_prewar)
with open(args.postwar_wordcount,'r') as ifd_postwar:
    dict_postwar = json.load(ifd_postwar)

print(len(dict_prewar))
with gzip.open(args.output,'wt') as ofd:
    for word,count in dict_prewar.items():
        if count > args.min_word_count and word in model_postwar.wv and word in model_prewar.wv:
            sims_prewar,sims_postwar = extraction(model_prewar,model_postwar,word,args.topn_words)
            word_dictionary = {
                word:{
                    'sims_prewar':sims_prewar,
                    'sims_postwar':sims_postwar
                    #'count':count,
                    #'neighborhood spread':spread(sims_prewar,sims_postwar),
                    #'percent overlap prewar and postwar':overlap(sims_prewar,sims_postwar)
                }
            }
            ofd.write(json.dumps(word_dictionary) + '\n')