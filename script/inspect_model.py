from gensim.models import Word2Vec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i',dest = 'input')
parser.add_argument('-w',dest = 'word')
parser.add_argument('-o',dest = 'output')
args = parser.parse_args()

model = Word2Vec.load(args.input)
sims = model.wv.most_similar(args.word,topn = 10)

print(sims)

# prewar
# [('wars', 0.7419632077217102), ('battle', 0.7300973534584045), ('fight', 0.71371990442276), ('victory', 0.7052441835403442), ('triumph', 0.6963124871253967), ('strife', 0.6853909492492676), ('rome', 0.684829831123352), ('law', 0.6778774261474609), ('feast', 0.6567040681838989), ('labour', 0.6559518575668335)]
# postwar
# [('battle', 0.884570300579071), ('work', 0.8347898125648499), ('present', 0.8317165970802307), ('peace', 0.8311308026313782), ('history', 0.8163361549377441), ('news', 0.8140602111816406), ('law', 0.8097506165504456), ('worst', 0.8096265196800232), ('state', 0.8083498477935791), ('birth', 0.8012677431106567)]