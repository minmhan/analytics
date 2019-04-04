# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:30:12 2018

@author: Min Han
"""

from flask_restplus import Api

from .spacyapi import api as sp
from .nltkapi import api as nltk
#from .stanfordapi import api as std
from .mongoapi import api as mongo
#from .flairapi import api as flair

api = Api(title='Analytics', version='1.0',description = 'Analytics Services')
api.namespaces.clear()

api.add_namespace(sp)
api.add_namespace(nltk)
#api.add_namespace(std)
api.add_namespace(mongo)
#api.add_namespace(flair)