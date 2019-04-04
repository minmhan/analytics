# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 14:07:48 2018

@author: Min Han
"""

from stanfordcorenlp import StanfordCoreNLP
import logging
import json

class StanfordNLP:
    def __init__(self, host='http://18.233.38.167',port=6789):
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000) 
        
        self.props = {
                'annotators':'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
                'pipelineLanguage':'en',
                'outputFormat':'json'
                }
        
    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)
    
    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)
    
    def ner(self, sentence):
        return self.nlp.ner(sentence)
    
    def parse(self, sentence):
        return self.nlp.parse(sentence)
    
    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)
    
    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))
    
    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                    'word': token['word'],
                    'lemma': token['lemma'],
                    'pos': token['pos'],
                    'ner': token['ner']
                    }
        return tokens