# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:57:11 2018

@author: Min Han
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MONGO_URI = os.environ.get('MONGO_CONNECTION_URI') or 'mongodb://permid:d0n0ldduck@13.228.187.243:27017/stradegi'
    MONGO_NEWS_COLLECTION = os.environ.get('MONGO_NEWS_COLLECTION') or 'news'
    
    NEO4J_CONNECTION_URI = os.environ.get('NEO4J_CONNECTION_URI') or 'bolt://13.228.187.243:7687'
    NEO4J_USER_NAME = os.environ.get('NEO4J_USER_NAME') or 'neo4j'
    NEO4J_USER_PASSWORD = os.environ.get('NEO4J_USER_PASSWORD') or 'password'
    