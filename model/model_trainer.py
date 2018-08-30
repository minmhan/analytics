# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 13:11:12 2018

@author: Min Han
"""

from pymongo import MongoClient
import plac
import random
from pathlib import Path
import spacy
import pickle

#[('Who is Min Min?', {'entities':[(7,14,'PERSON')]})]
TRAIN_DATA = []

def getTrainData():
    client = MongoClient('mongodb://tesla:d0n0ldduck@18.233.38.167', 27017)
    db = client.text
    cursor = db.trit.find({"$or":[{"sentences.instances.Type":"e/Company"},
                                  {"sentences.instances.Type":"e/Organization"}]}, 
                            {"sentences":1}).skip(10).limit(5)
    
    for c in cursor:
        for s in c.get("sentences"):
            entities = []
            for i in s.get("instances"):
                if(i.get("Type") == "e/Company" or i.get("Type") == "e/Organization"):
                    offset = i.get("Offset")
                    length = i.get("Length")
                    entities.append((offset, offset+length, 'ORG'))
            if entities:
                TRAIN_DATA.append((s.get("text"), {'entities':entities }))
        print("loading...")
               

def saveTrainData():
    with open('TRAIN_DATA2', 'wb') as fp:
        pickle.dump(TRAIN_DATA, fp)


TRAIN_DATA2 = []
def loadTrainData():
    with open ('D:\Research\Python\Analysis\model\TRAIN_DATA2', 'rb') as fp:
        TRAIN_DATA2 = pickle.load(fp)
        print("loaded...")


def main():
    skip = 450
    take = 5
    nextRec = True
    client = MongoClient('mongodb://tesla:d0n0ldduck@18.233.38.167', 27017)
    db = client.text
    
    while nextRec:
        TRAIN_DATA.clear()
        cursor = db.trit.find({"$or":[{"sentences.instances.Type":"e/Company"},
                                      {"sentences.instances.Type":"e/Organization"}]}, 
                                {"sentences":1}).skip(skip).limit(take)
        #print(cursor.count(True))
        if(cursor.count(True) == 0):
            nextRec = False
            print("End of Record")
            
        for c in cursor:
            for s in c.get("sentences"):
                entities = []
                for i in s.get("instances"):
                    if(i.get("Type") == "e/Company" or i.get("Type") == "e/Organization"):
                        offset = i.get("Offset")
                        length = i.get("Length")
                        entities.append((offset, offset+length, 'ORG'))
                if entities:
                    TRAIN_DATA.append((s.get("text"), {'entities':entities }))
        skip += take
        
        train()
        print("Total Finish Training Records '%s'" % skip)
        print("next...")
        


@plac.annotations(
        model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
        output_dir=("Optional output directory", "option", "o", Path),
        n_iter=("Number of training iterations", "option", "n", int))
def train(model="D:\Research\Python\Analysis\model\org", output_dir="D:\Research\Python\Analysis\model\org", n_iter=30):
    print("Train record count '%s'" % len(TRAIN_DATA))    
    
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')
        print("Created blank 'en' model")
        
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe('ner')
        
    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])
            
            
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training(device=0)
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations],drop=0.5, sgd=optimizer, losses=losses)
            print(losses)
            
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
    
    
def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 1e-8  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 1e-8  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f_score = 2 * (precision * recall) / (precision + recall)
    return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}
            
if __name__ == '__main__':
    #plac.call(main)
    main()