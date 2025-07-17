from gensim.models import Word2Vec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i',dest = 'input')
parser.add_argument('-w',dest = 'word')
parser.add_argument('-o',dest = 'output')
args = parser.parse_args()

model = Word2Vec.load(args.input)
sims = model.wv.most_similar(args.word,topn = 10)

#print(sims)

print('hello world')