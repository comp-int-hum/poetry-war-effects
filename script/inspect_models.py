from gensim.models import Word2Vec
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--prewar_model',dest = 'prewar_model',help = 'trained prewar model')
parser.add_argument('--postwar_model',dest = 'postwar_model',help = 'trained postwar model')
parser.add_argument('--prewar_wordcount',dest = 'prewar_wordcount',help = 'dictionary of words used in prewar poetry')
parser.add_argument('--postwar_wordcount',dest = 'postwar_wordcount',help = 'dictionary of words used in postwar poetry')
parser.add_argument('--word',dest = 'word',help = 'this is the word to examine')
args = parser.parse_args()

model_prewar = Word2Vec.load(args.prewar_model)
model_postwar = Word2Vec.load(args.postwar_model)

def measurement(model1,model2,word):
    sims_prewar = model1.wv.most_similar(word,topn = 10)
    prewar_scores = []
    for top_word,score in sims_prewar:
        prewar_scores.append(score)
    prewar_neighborhood_cluster = max(prewar_scores) - min(prewar_scores)

    sims_postwar = model2.wv.most_similar(word,topn = 10)
    postwar_scores = []
    for top_word,score in sims_postwar:
        postwar_scores.append(score)
    postwar_neighborhood_cluster = max(postwar_scores) - min(postwar_scores)

    return {'prewar':prewar_neighborhood_cluster,'postwar':postwar_neighborhood_cluster}


with open(args.prewar_wordcount,'r') as ifd_prewar:
    dict_prewar = json.load(ifd_prewar)
with open(args.postwar_wordcount,'r') as ifd_postwar:
    dict_postwar = json.load(ifd_postwar)

print(model_prewar.wv.most_similar('his',topn=10))
for word,count in dict_prewar.items():
    if count > 5000 and word in model_postwar.wv and word in model_prewar.wv:
        print(word,count)
        print(word,measurement(model_prewar,model_postwar,word))