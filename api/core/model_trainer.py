# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 10:22:35 2018

@author: Min Han
"""

import plac
import random
from pathlib import Path
import spacy

# training data
TRAIN_DATA = [
        ('Who is Min Min?', {
                'entities':[(7,14,'PERSON')]}),
        ('I like Mandalay.', {
                'entities':[(7,15,'LOC')]})
        ]


@plac.annotations(
        model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
        output_dir=("Optional output directory", "option", "o", Path),
        n_iter=("Number of training iterations", "option", "n", int))
def main(model="en_core_web_sm", output_dir="D:\Research\Python\Analysis", n_iter=100):
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
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations],drop=0.5, sgd=optimizer, losses=losses)
            print(losses)
            
    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
        print('Tokens', [(t.text, t.ent_type_,t.ent_iob) for t in doc])
        
    # Save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
        
        # Test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
            
            
if __name__ == '__main__':
    plac.call(main)