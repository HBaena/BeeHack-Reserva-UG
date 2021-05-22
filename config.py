import os
from os import path, getcwd

from flask import Flask
from flask_restful import Api  # modules for fast creation of apis
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# def connect_to_sqlite(filename):
#     return SqliteConnection(path.join(getcwd(), filename))


app = Flask(__name__)  # Creating flask app
app.secret_key = "gydasjhfuisuqtyy234897dshfbhsdfg83wt7"

api = Api(app)  # Creating API object from flask app

PWD = os.path.abspath(os.curdir)    
db_name = 'beehack.db'
uri = 'sqlite:///{}/{}'.format(PWD, db_name)# print(uri)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/{}'.format(PWD, db_name)# print(uri)
# SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.create_all()
