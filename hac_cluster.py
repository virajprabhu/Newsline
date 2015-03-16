# Author : Animesh Das , Sujay Narumanchi , Shruti Rijhwani , Viraj Prabhu
# Information Retrieval Project - Group 6
# Libraries Used : 
#               python sklearn
#               python scrapy 
#               python selenium


# Due thanks to the example :
# Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Lars Buitinck <L.J.Buitinck@uva.nl>
# License: BSD 3 clause

from __future__ import print_function

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, MiniBatchKMeans, MeanShift, estimate_bandwidth
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift, estimate_bandwidth
import logging
from optparse import OptionParser
import sys
from time import time
import os
import string
import numpy as np
import nltk
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster.hierarchical import _hc_cut
from sklearn.metrics import silhouette_score
from sklearn.externals import joblib
import json
import sys

if not len(sys.argv) == 2 :
  print("Error No Arguments Supplied ")
  exit(1)

path = sys.argv[1] 

token_dict = {}
stemmer = nltk.PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

for subdir, dirs, files in os.walk(path):
    for file in files:
        file_path = subdir + os.path.sep + file
        document = open(file_path, 'r')
        text = document.read()
        lowers = text.lower()
        no_punctuation = lowers.translate(None, string.punctuation)
        token_dict[file] = no_punctuation

print("No of files = " + str(len(token_dict.keys()))) 
print("TfidfVectorizer starting ...") 
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values ())
tfs = tfs.todense() 

joblib.dump(tfs, 'tfs.pkl')
print("Removed Stop Words , Stemmed and calculated Tf-Idf Values") 


linkage = 'ward' # 'complete' and 'average'

print("Starting Agglomerative Clustering using single linkage distance measure ...") 
clustering = AgglomerativeClustering(linkage=linkage, n_clusters=1 , compute_full_tree = True)
clustering.fit(tfs)
joblib.dump(clustering,'clustering.pkl')
print("HAC complete, Full_tree computed ")


print("Calculating the best value for the number of Clusters using Silhouette Score as the evaluation metric")
bestScore = float("-inf")
bestNumber = -10
for numberClusters in range(2,len(token_dict.keys())):
  clustering.labels_ = _hc_cut(numberClusters, clustering.children_ ,clustering.n_leaves_)
  silhouetteScore = silhouette_score(tfs, clustering.labels_)
  if silhouetteScore > bestScore:
    bestScore = silhouetteScore
    bestNumber = numberClusters

print("Calculated the best value for number of Clusters = " + str(bestNumber))
numberOfClusters = bestNumber
finalDictionary = {}

clustering.labels_ = _hc_cut(numberOfClusters, clustering.children_ ,clustering.n_leaves_)

for i in range(numberOfClusters):
  finalDictionary[i] = []

for i in range(len(clustering.labels_)):
  finalDictionary[clustering.labels_[i]].append(token_dict.keys()[i])

json.dump(finalDictionary, open('finalDictionary.json', 'w'))
print("Completed")

finalClusters = open('finalClusters.txt', 'w')


for key in finalDictionary.keys():
  print("Cluster " + str(key) + ":")
  finalClusters.write("Cluster " + str(key) + ":\n")
  for element in finalDictionary[key]:
    print('\t' + element )
    finalClusters.write('\t' + element + '\n')
  print()
  finalClusters.write('\n')

finalClusters.close()


greatClusters = open('greatClusters.txt', 'w')
for key in finalDictionary.keys():
  if len(finalDictionary[key]) > 1:
    greatClusters.write("Cluster " + str(key) + ":\n")
    for element in finalDictionary[key]:
      greatClusters.write('\t' + element + '\n')
    greatClusters.write('\n')

greatClusters.close()

