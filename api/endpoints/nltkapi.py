# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 18:04:35 2018

@author: Min Han
"""

from flask_restplus import Namespace, Resource, fields

from core import NltkModel

api = Namespace('Nltk', description='Nltk NLP APIs')
    
nltk = api.model('Nltk', {
    'text': fields.String(required=True, description='The task details')
})

parser = api.parser()
parser.add_argument('text', type=str, required=True, help = 'input text')

@api.route('/hypernym/<string:text>')
class GetHypernym(Resource):
    def get(self, text):
        sp = NltkModel()
        hyper = sp.getHypernym(text)
        return hyper

@api.route('/hypernym/')
class Hypernym(Resource):
    @api.expect(nltk)
    def post(self):
        p = api.payload
        sp = NltkModel()
        hyper = sp.getHypernym(p['text'])
        return hyper