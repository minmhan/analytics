# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 21:20:21 2018

@author: minmh
"""

from flask import Flask
from endpoints import api
from config import Config

app = Flask(__name__)
#app.config.from_object(Config)
#mongo = PyMongo(app)

api.init_app(app)
    
if __name__ == "__main__":
    app.run(threaded=True)
    