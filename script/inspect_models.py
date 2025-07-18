from gensim.models import Word2Vec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i1','--input_prewar',dest = 'input_prewar',help = 'trained prewar model')
parser.add_argument('-i2','--input_postwar',dest = 'input_postwar',help = 'trained postwar model')
parser.add_argument('-w',dest = 'word',help = 'this is the word to examine')
args = parser.parse_args()

model_prewar = Word2Vec.load(args.input_prewar)
model_postwar = Word2Vec.load(args.input_postwar)
sims_prewar = model_prewar.wv.most_similar(args.word,topn = 10)
sims_postwar = model_postwar.wv.most_similar(args.word,topn = 10)

print(sims_prewar)
print(sims_postwar)