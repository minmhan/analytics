# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:03:54 2018

@author: Min Han
"""
import spacy

class SpacyModel(object):
    def __init__(self, m):
        self.nlp = spacy.load(m)

        
    def getSentences(self, s):
        doc = self.nlp(s)
        sents = []
        for s in doc.sents:
            sents.append(str(s))
                        
        return sents


    def getPOS(self, s):
        doc = self.nlp(s)
        token = []
        for t in doc:
            token.append({ "text" : t.text, "lemma": t.lemma_, "pos":t.pos_, 
                          "tag":t.tag_, "dep":t.dep_,"shape":t.shape_,
                          "isAlpha":t.is_alpha, "isStop":t.is_stop })
        return token
    
    
    def getDependency(self, s):
        doc = self.nlp(s)
        chunks = []
        for c in doc.noun_chunks:
            chunks.append({ "text": c.text, "rootText": c.root.text, "rootDep": c.root.dep_, "rootHeadText": c.root.head.text })
        
        return chunks
    
    
    def getEntity(self, s):
        doc = self.nlp(s)
        ent = []
        for e in doc.ents:
            ent.append({ "text": e.text, "start": e.start_char, "end":e.end_char, "label":e.label_})
        return ent
    
    def getOrg(self, s):
        doc = self.nlp(s)
        org = []
        for e in doc.ents:
            org.append({ "text": e.text, "start": e.start_char, "end":e.end_char, "label":e.label_})
        return org
    

    def getNounChunk(self, s):
        doc = self.nlp(s)
        chunks = []
        for c in doc.noun_chunks:
            chunks.append({ "text": c.text, "root": c.root.text, "dep":c.root.dep_ })
        
        return chunks
    