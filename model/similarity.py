# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:15:00 2018

@author: Min Han
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
from pymongo import MongoClient
import unicodedata

# Mongo Connection
client = MongoClient('mongodb://tesla:d0n0ldduck@18.233.38.167', 27017)
db = client.text

def process(str):
    # remove accented characters
    str = unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8','ignore')

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


def remove_special_characters(text, remove_digits=False):
    pattern =r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def cos_sim(a,b):
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)


def getSimilarity(dict1, dict2):
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
    return cos_sim(v1,v2)


if __name__ == '__main__':
    dict1 = process("To join a dynamic working environment")
    dict2 = process("To join a dynamic work environment. Min Min")
    print(getSimilarity(dict1,dict2))
    