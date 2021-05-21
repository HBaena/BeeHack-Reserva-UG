from flask import request  # Flask, receiving data from requests, json handling
from flask import send_file  # Create url from statics files
from flask import jsonify  # Flask, receiving data from requests, json handling
from flask import after_this_request  
from flask_restful import Resource  # modules for fast creation of apis

from config import app
from config import api
from config import jwt
from config import connect_to_db_from_json
from config import init_alpr

from typing import Any, NoReturn

from os import getcwd
from os import path 
from os import remove 

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from time import time

from icecream import ic

API_VERSION = '1.0.000'
pool = None

@app.after_request
def after_request(response) -> Any:
    """
    Prevent CORS problems after each request
    :param response: Response of any request
    :return: The same request
    """

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE, PATCH')
    return response

@app.before_first_request
def initialize() -> NoReturn:
    global pool

    pool = connect_to_db_from_json("db.json")