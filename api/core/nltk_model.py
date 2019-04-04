# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:36:50 2018

@author: Min Han
"""

from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk

class NltkModel(object):
    def __init__(self):
        pass
    
    def getHypernym(self, str):
        syns = wordnet.synsets(str)
        df = []
        for s in syns:
            hy = s.hypernyms()
            hyper = [{ "name": h.lemmas()[0].name(), "definition": h.definition() } for h in hy]          
            df.append({ "name": s.lemmas()[0].name(), "definition": s.definition(), "hypernyms": hyper })
            
        return df
    
    def getSisterTerms(self, str):
        syns = wordnet.synsets(str)
        return ''
    
    def getSimilarity(self, dict1, dict2):
        all_words_list = []
        for key in dict1:
            all_words_list.append(key)
        for key in dict2:
            all_words_list.append(key)
        all_words_list_size = len(all_words_list)
        
        v1 = np.zeros(all_words_list_size, dtype=np.int)
        v2 = np.zeros(all_words_list_size, dtype=np.int)
        i = 0
        for (key) in all_words_list:
            v1[i] = dict1.get(key, 0)
            v2[i] = dict2.get(key, 0)
            i = i + 1
            
        return self.cos_sim(v1,v2)

    
    def process(self, str):
        tokens = word_tokenize(str)
        words = [w.lower() for w in tokens]
        
        porter = nltk.PorterStemmer()
        stemmed_tokens = [porter.stem(t) for t in words]
        
        # remove stop words
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]
        
        # count words
        count = nltk.defaultdict(int)
        for word in filtered_tokens:
            count[word] += 1
        return count;


    def cos_sim(self, a, b):
        dot_product = np.dot(a,b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)