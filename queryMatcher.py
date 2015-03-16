# Author : Animesh Das , Sujay Narumanchi , Shruti Rijhwani , Viraj Prabhu
# Information Retrieval Project - Group 6
# Libraries Used : 
#               python sklearn
#               python scrapy 
#               python selenium

from __future__ import print_function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords
import os
import string
import numpy as np
import nltk
import sys
import logging
import numpy.linalg as LA
import math
import json

token_dict = {}
stemmer = nltk.PorterStemmer()

def stem_tokens(tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = tokens#stem_tokens(tokens, stemmer)
    return stems

def queryMatcher(query, path):
    print ("Entered query Matcher")
    stopWords = stopwords.words('english')
    
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_path = subdir + os.path.sep + file
            #print("Filepath:" + str(file_path))
            document = open(file_path, 'r')
            text = document.read()
            lowers = text.lower()
            no_punctuation = lowers.translate(None, string.punctuation)
            token_dict[file] = no_punctuation
            document.close()

    print ("Query is " + query)
    query = [query]
    tfidfTrain = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    trainVectorizer = tfidfTrain.fit_transform(token_dict.values ())
    trainVectorizerArray = trainVectorizer.toarray()
    testVectorizer = tfidfTrain.transform(query);
    testVectorizerArray = testVectorizer.toarray()

    print ("Fit Vectorizer to train set\n", trainVectorizer)
    print ("Transform Vectorizer to test set\n", testVectorizer)
    
    cx = lambda a, b : round(np.inner(a, b)/(LA.norm(a)*LA.norm(b)), 3)

    maxcos = 0.0

    #print("Test vector is:" + str(testVectorizerArray[0]))
    print("Fetching search results...")
##    if(LA.norm(testVectorizerArray[0]) == 0):
##        return (None, None)
    
    for index, vector in enumerate(trainVectorizerArray):
        #print("Vector is:" + str(vector))
        cosine = cx(vector, testVectorizerArray[0])
        if((not math.isnan(cosine)) and cosine > maxcos):
            maxpos = index
            maxcos = cosine
        print("Cosine is:" + str(cosine))
    if(maxcos == 0):
        print ("No matches found!\n")
    else:
        print("Closest match:" + str(token_dict.keys()[maxpos]) + " with cosine:" + str(maxcos))
    
        if(maxcos == 0):
            print ("NO MATCH")
            return(None, None)
        
        finalDictionary = open('finalDictionary.json', 'r')
        finalDict= json.load(finalDictionary)

        values = finalDict.values()
        for valueList in values:
            if str(token_dict.keys()[maxpos]) in valueList:
                return (str(token_dict.keys()[maxpos]), valueList)
                

    
    
