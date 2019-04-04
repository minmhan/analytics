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

sp = SpacyModel("en_core_web_sm")
#sp_org = SpacyModel("en_permid_org_ner")

@api.route('/sentence/<string:text>')
class GetSentence(Resource):
    def get(self, text):
        sentences = sp.getSentences(text)
        return sentences

@api.route('/sentence/')
class Sentence(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        sentences = sp.getSentences(p['text'])
        return sentences
               
@api.route('/pos/<string:text>')
class GetPos(Resource):
    def get(self, text):
        pos = sp.getPOS(text)
        return pos

@api.route('/pos/')
class Pos(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        pos = sp.getPOS(p['text'])
        return pos


@api.route('/dep/<string:text>')
class GetDependency(Resource):
    @api.doc("get dependency")
    def get(self, text):
        dep = sp.getDependency(text)
        return dep

@api.route('/dep/')
class Dependency(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        dep = sp.getDependency(p['text'])
        return dep
    
@api.route('/ent/<string:text>')
class GetEnt(Resource):
    def get(self, text):
        ent = sp.getEntity(text)
        return ent
    
@api.route('/ent/')
class Ent(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        ent = sp.getEntity(p['text'])
        return ent

#
#@api.route('/org/')
#class Org(Resource):
#    @api.expect(spacy)
#    def post(self):
#        p = api.payload
#        org = sp_org.getOrg(p['text'])
#        return org
    
    
@api.route('/nounchunk')
class NounChunk(Resource):
    @api.expect(spacy)
    def post(self):
        p = api.payload
        nounchunks = sp.getNounChunk(p['text'])
        return nounchunks
    
