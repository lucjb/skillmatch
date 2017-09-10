import sys
import numpy as np
from scipy import spatial

import argparse

parser = argparse.ArgumentParser(description='Searches mentors and words, associated to given queries.')
parser.add_argument('-w', help='Searches for words, rather than mentors', action='store_true', dest='search_words')
parser.add_argument('-q', help='Searches the given query. If not provided, a list of test queries is used', dest='query')
parser.add_argument('-e', help='Runs evaluation test', dest='evaluation', action='store_true')
args = parser.parse_args()


search_words, query, evaluation = args.search_words, args.query, args.evaluation

word2vec = {}
embeddings = open('enron_embeddings5.csv')
_, dim = embeddings.next().split()
dim = int(dim)
for line in embeddings:
	wordvec = line.split()
	word = wordvec[0]
	vec = np.array(map(float, wordvec[1:]))
	word2vec[word]=vec

target = word2vec

if not search_words:	
	mentor2vec = {}
	mentor_vec = open('profiles.csv')
	for line in mentor_vec:
		mentorvec = line.split()
		mentor = mentorvec[0]
		vec = np.array(map(float, mentorvec[1:]))
		mentor2vec[mentor]=vec

	target = mentor2vec
	




def find(query):
	query_vec = np.zeros(dim)
	for s in query.split():
		query_vec += word2vec[s.lower()]

	word_scores = []
	for word, vec in target.iteritems():
		score = spatial.distance.cosine(query_vec, vec)
		word_scores.append((score, word))

	return sorted(word_scores)

def evaluate():
	queries = {
	'trading': ['kitchen-l', 'zipper-a', 'dean-c', 'scholtes-d', 'baughman-d', 'bass-e', 'saibi-e', 'schwieger-j', 'quenet-j', 'stepenovitch-j', 'forney-j', 'ruscitti-k', 'swerzbin-m', 'slinger-r', 'kuykendall-t'], 
	'legal':['haedicke-m', 'derrick-j'],
	'law': ['haedicke-m', 'derrick-j'], 
	'legal affairs':['haedicke-m'],
	'risk':['causholli-m', 'buy-r', 'kaminski-v'],
	'risk management':['causholli-m', 'buy-r', 'kaminski-v'],
	'Government Affairs':['steffes-j', 'dasovich-j'],
	'Government':['steffes-j', 'dasovich-j'],
	'governmental affairs':['steffes-j', 'dasovich-j'],
	'logistics':['farmer-d'],
	'gas': ['horton-s'],
	'pipeline': ['hyatt-k', 'horton-s']

	}

	hits = 0.
	total = 0.
	for q, e in queries.iteritems():
		r = zip(*find(q)[:5])[1]
		total += len(r)
		for c in r:
			for ei in e:
				if ei in c:
					hits+=1
	print 'Precision@5', hits/total


queries = ['pricing', 'risk management', 'argentina', 'accounting', 'god', 'human resources', 'nuclear energy', 'linux sql', 'computers', 'telecommunications', 'legal affairs', 'hiring', 'project management', 'trading', 'finance', 'marketing', 'renewable energy', 'solar energy', 'paper', 'media']

#queries = ['Regulatory Affairs', 'Logistics', 'Risk Management', 'legal', 'Government Affairs', 'Cash']

if query:
	print zip(*find(query)[:10])[1]
elif evaluation:
	evaluate()
else:
	for query in queries:
		print query
		print zip(*find(query)[:10])[1]
		print '============================='



