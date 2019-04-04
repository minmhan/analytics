# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:08:30 2018

@author: Min Han
"""

from flask_restplus import Namespace, Resource, fields

from core import StanfordNLP

api = Namespace('Stanford', description='Stanford NLP APIs')
    
nltk = api.model('Stanford', {
    'text': fields.String(required=True, description='The task details')
})


parser = api.parser()
parser.add_argument('text', type=str, required=True, help = 'input text')

@api.route('/ent/<string:text>')
class GetEnt(Resource):
    def get(self, text):
        s = StanfordNLP()
        ent = s.ner(text)
        return ent