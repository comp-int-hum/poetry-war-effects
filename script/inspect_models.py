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

def measurement(model1,model2,word):
    model_prewar = Word2Vec.load(model1)
    model_postwar = Word2Vec.load(model2)

    sims_prewar = model_prewar.wv.most_similar(word,topn = 10)
    prewar_scores = []
    for word,score in sims_prewar:
        prewar_scores.append(score)
    prewar_neighborhood_cluster = max(prewar_scores) - min(prewar_scores)

    sims_postwar = model_postwar.wv.most_similar(word,topn = 10)
    postwar_scores = []
    for word,score in sims_postwar:
        postwar_scores.append(score)
    postwar_neighborhood_cluster = max(postwar_scores) - min(postwar_scores)

    return {'prewar':prewar_neighborhood_cluster,'postwar':postwar_neighborhood_cluster}


with open(args.prewar_wordcount,'r') as ifd_prewar:
    dict_prewar = json.load(ifd_prewar)
with open(args.postwar_wordcount,'r') as ifd_postwar:
    dict_postwar = json.load(ifd_postwar)

if dict_prewar[args.word] < 10 or dict_postwar[args.word] < 10:
    print('Insufficient use of word. Please choose another word.')
else:
    print(measurement(args.input_prewar,args.input_postwar,args.word))