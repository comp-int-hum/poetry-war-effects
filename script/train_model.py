from gensim.models import Word2Vec
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i',dest = 'input')
parser.add_argument('-o',dest = 'output')
args = parser.parse_arguments()