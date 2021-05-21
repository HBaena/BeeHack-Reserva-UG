from flask import Flask
from flask_restful import Api  # modules for fast creation of apis
from os import path, getcwd
from DB import PosgresPoolConnection
from psycopg2 import pool
from flask_jwt_extended import JWTManager
from datetime import timedelta
from alpr import ALPR

def connect_to_db_from_json(filename: str) -> pool:
    return PosgresPoolConnection(path.join(getcwd(), filename))

def init_alpr() -> ALPR:
    return ALPR(path.join(getcwd(), "alpr.json"))

app = Flask(__name__)  # Creating flask app
app.secret_key = "gydasjhfuisuqtyy234897dshfbhsdfg83wt7"
api = Api(app)  # Creating API object from flask app
# jwt.
app.config['JWT_SECRET_KEY'] = 'sinttemporirureduis'
app.config['JWT_PUBLIC_KEY'] = 'Minimconsecteturineucillum'
app.config['JWT_PRIVATE_KEY'] = 'doloressecupidatat'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)