# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:33:37 2018

@author: Min Han
"""

from flask_restplus import Namespace, Resource, fields

from core import SpacyModel

api = Namespace('SpaCy', description='SpaCy NLP APIs')
    
spacy = api.model('Spacy', {
    'text': fields.String(required=True, description='The task details')
})

parser = api.parser()
parser.add_argument('text', type=str, required=True, help = 'input text')

@api.route('/sentence/<string:text>')
class GetSentence(Resource):
    def get(self, text):
        sp = SpacyModel()
        sentences = sp.getSentences(text)
        return sentences

@api.route('/sentence/')
class Sentence(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        sp = SpacyModel()
        sentences = sp.getSentences(p['text'])
        return sentences
               
@api.route('/pos/<string:text>')
class GetPos(Resource):
    def get(self, text):
        sp = SpacyModel()
        pos = sp.getPOS(text)
        return pos


@api.route('/pos/')
class Pos(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        sp = SpacyModel()
        pos = sp.getPOS(p['text'])
        return pos


@api.route('/dep/<string:text>')
class GetDependency(Resource):
    @api.doc("get dependency")
    def get(self, text):
        sp = SpacyModel()
        dep = sp.getDependency(text)
        return dep

@api.route('/dep/')
class Dependency(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        sp = SpacyModel()
        dep = sp.getDependency(p['text'])
        return dep
    
@api.route('/ent/<string:text>')
class GetEnt(Resource):
    def get(self, text):
        sp = SpacyModel()
        ent = sp.getEntity(text)
        return ent
    
@api.route('/ent/')
class Ent(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        sp = SpacyModel()
        ent = sp.getEntity(p['text'])
        return ent
