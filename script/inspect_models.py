from gensim.models import Word2Vec
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-i1','--input_prewar',dest = 'input_prewar',help = 'trained prewar model')
parser.add_argument('-i2','--input_postwar',dest = 'input_postwar',help = 'trained postwar model')
parser.add_argument('-i3','--prewar_wordcount',dest = 'prewar_wordcount',help = 'dictionary of words used in prewar poetry')
parser.add_argument('-i4','--postwar_wordcount',dest = 'postwar_wordcount',help = 'dictionary of words used in postwar poetry')
parser.add_argument('-w',dest = 'word',help = 'this is the word to examine')
args = parser.parse_args()

model_prewar = Word2Vec.load(args.input_prewar)
model_postwar = Word2Vec.load(args.input_postwar)

with open(args.prewar_wordcount,'r') as ifd_prewar:
    dict_prewar = json.load(ifd_prewar)
with open(args.postwar_wordcount,'r') as ifd_postwar:
    dict_postwar = json.load(ifd_postwar)

if dict_prewar[args.word] < 10 or dict_postwar[args.word] < 10:
    print('Insufficient use of word. Please choose another word.')
else:
    sims_prewar = model_prewar.wv.most_similar(args.word,topn = 10)
    sims_postwar = model_postwar.wv.most_similar(args.word,topn = 10)
    print(sims_prewar)
    print(sims_postwar)