"""
Created on Thu March 29 17:35:08 2019

ref: https://github.com/zalandoresearch/flair
"""

from flask_restplus import Namespace, Resource, fields
from flair.data import Sentence
from flair.models import SequenceTagger

api = Namespace('Flair', description='Flair NLP APIs')
    
spacy = api.model('Flair', {
    'text': fields.String(required=True, description='The task details')
})

parser = api.parser()
parser.add_argument('text', type=str, required=True, help = 'input text')

pos_tagger = SequenceTagger.load('pos-fast')
chunk_tagger = SequenceTagger.load('chunk-fast')

@api.route('/pos/<string:text>')
class GetPos(Resource):
    def get(self, text):
        sentence = Sentence(text)
        pos_tagger.predict(sentence)
        return sentence.to_tagged_string()
    

@api.route('/chunk/<string:text>')
class GetChunk(Resource):
    def get(self, text):
        sentence = Sentence(text)
        chunk_tagger.predict(sentence)
        return sentence.to_tagged_string()