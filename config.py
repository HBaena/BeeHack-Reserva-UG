import os
from os import path, getcwd

from datetime import timedelta

from flask import Flask
from flask_restful import Api  # modules for fast creation of apis

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

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

# jwt.
app.config['JWT_SECRET_KEY'] = 'sinttemporirureduis'
app.config['JWT_PUBLIC_KEY'] = 'Minimconsecteturineucillum'
app.config['JWT_PRIVATE_KEY'] = 'doloressecupidatat'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)