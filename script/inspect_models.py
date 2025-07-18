from gensim.models import Word2Vec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i1','--input1',dest = 'input1')
parser.add_argument('-i2','--input2',dest = 'input2')
parser.add_argument('-w',dest = 'word')
args = parser.parse_args()

model_prewar = Word2Vec.load(args.input1)
model_postwar = Word2Vec.load(args.input2)
sims_prewar = model_prewar.wv.most_similar(args.word,topn = 10)
sims_postwar = model_postwar.wv.most_similar(args.word,topn = 10)

print(sims_prewar)
print(sims_postwar)