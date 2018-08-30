# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 17:35:08 2018

@author: Min Han
"""

from flask_restplus import Namespace, Resource

from pymongo import MongoClient


api = Namespace('Mongo', description='Mongo APIs')

# Mongo Connection
client = MongoClient('mongodb://tesla:d0n0ldduck@18.233.38.167', 27017)
db = client.text

@api.route('/document/<string:text>')
class Document(Resource):
    def get(self, text):
        #a = mongo.db.news.find({"url":"http://www.reuters.com/article/brief-edelweiss-financial-services-says/brief-edelweiss-financial-services-says-edelweiss-retail-finance-to-issue-ncds-worth-up-to-5-bln-rupees-idUSFWN1QP003"})
        return text