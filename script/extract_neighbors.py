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

with open(args.prewar_wordcount,'r') as ifd_prewar,open(args.postwar_wordcount,'r') as ifd_postwar:
    dict_prewar = json.load(ifd_prewar)
    dict_postwar = json.load(ifd_postwar)

all_words = set(dict_prewar.keys() | dict_postwar.keys())

with gzip.open(args.output,'wt') as ofd:
    for word in all_words:
        if dict_prewar.get(word,0) > args.min_word_count and dict_postwar.get(word,0) > args.min_word_count:
            sims_prewar,sims_postwar = extraction(model_prewar,model_postwar,word,args.topn_words)
            word_dictionary = {
                word:{
                    'sims_prewar':sims_prewar,
                    'sims_postwar':sims_postwar
                }
            }
            ofd.write(json.dumps(word_dictionary)+ '\n')