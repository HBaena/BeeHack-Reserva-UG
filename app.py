from flask import request  # Flask, receiving data from requests, json handling
from flask import send_file  # Create url from statics files
from flask import jsonify  # Flask, receiving data from requests, json handling
from flask import after_this_request  
from flask_restful import Resource  # modules for fast creation of apis

from config import app
from config import api
from config import db
# from config import connect_to_sqlite

from functions import generate_qr_from_json
from functions import decode_qr_code

from model import Model

from typing import Any, NoReturn

from os import getcwd
from os import path 
from os import remove 

from datetime import datetime
from datetime import timedelta
from datetime import timezone


from json import loads
from time import time
from icecream import ic
import io

from sqlalchemy import inspect
# from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy import inspect


API_VERSION = '1.0.000'
pool = None
model = None
inspector = None

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
    global model, inspector
    model = Model(db.session)
    db.create_all()
    db.session.commit()
    # model.insert_user( 
    #     username='HBaena', full_name='Adan Hernandez Baena', 
    #     password='psw', email='ahernandezbaena@ugto.mx', 
    #     user_type='Estudiante', career='Sistemas',
    #     division='dicis')


class Main(Resource):

    def get(self):
        ic(model.execute('SELECT * FROM "User"'))
        return jsonify(version=API_VERSION)


class User(Resource):
    def get(self):
        idx = request.args.get('idx', None)
        if idx:
            response = model.read_user(idx)
        else:
            response = model.read_all_users()

        if response:
            return jsonify(status="good", message="Read correctly", 
                data=response)
        else:
            return jsonify(status="fail", message="Error whil reading")

    def post(self):
        data_db = dict(
            username=request.form.get('username', None), 
            full_name=request.form.get('full_name', None), 
            password=request.form.get('password', None), 
            email=request.form.get('email', None), 
            user_type=request.form.get('user_type', None), 
            career=request.form.get('career', None),
            division=request.form.get('division', None)
            )
        if not all(data_db.values()):
            return jsonify(status="error", message="All fields are required")
        response = model.insert_user(**data_db)
        if response:
            return jsonify(status="good", message="Inserted correctly", 
                data=dict(user_id=response))
        else:
            return jsonify(status="fail", message="Error whil inserting")

    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_user(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")


class Event(Resource):
    def get(self):
        idx = request.args.get('idx', None)
        if idx:
            response = model.read_event(idx)
        else:
            response = model.read_all_events()

        if response:
            return jsonify(status="good", message="Read correctly", 
                data=response)
        else:
            return jsonify(status="fail", message="Error whil reading")

    def post(self):
        data_db = dict(
            name=request.form.get('name', None),
            description=request.form.get('description', None),
            topic=request.form.get('topic', None),
            hour_begin=request.form.get('hour_begin', None),
            duration=request.form.get('duration', None),
            speaker=request.form.get('speaker', None),
            credits=request.form.get('credits', None),
            credit_type=request.form.get('credit_type', None),
            qr_code_begin=request.form.get('qr_code_begin', None),
            qr_code_end=request.form.get('qr_code_end', None),
            room_id=request.form.get('room_id', None),
            user_id=request.form.get('user_id', None)
           )

        response = model.insert_event(**data_db)
        if response:
            return jsonify(status="good", message="Inserted correctly", 
                data=dict(event_id=response))
        else:
            return jsonify(status="fail", message="Error whil inserting")

    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_event(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")


class Room(Resource):
    def get(self):
        idx = request.args.get('idx', None)
        if idx:
            response = model.read_room(idx)
        else:
            response = model.read_all_rooms()

        if response:
            return jsonify(status="good", message="Read correctly", 
                data=response)
        else:
            return jsonify(status="fail", message="Error whil reading")

    def post(self):
        data_db = dict(
            size=request.form.get("size", None), 
            name=request.form.get("name", None), 
            description=request.form.get("description", None), 
            building=request.form.get("building", None), 
            division=request.form.get("division", None), 
            campus=request.form.get("campus", None)
           )
        response = model.insert_room(**data_db)
        if response:
            return jsonify(status="good", message="Inserted correctly", 
                data=dict(room_id=response))
        else:
            return jsonify(status="fail", message="Error whil inserting")

    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_room(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")

class QRCode(Resource):

    def get(self):

        data = dict(request.args)
        ic(data)
        try:
            qr_code = generate_qr_from_json(data)
        except Exception as e:
            return jsonify(status='error', message='Error creating code', log=str(e))

        img_byte_arr = io.BytesIO()
        qr_code.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return send_file(
            io.BytesIO(img_byte_arr),
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename='qr_code.jpg')

    def post(self):

        qr_code = request.files.get("qr-code", None)
        if not qr_code:
            return jsonify(status='error', message='idx not received')
        return loads(decode_qr_code(qr_code.read()))


api.add_resource(Main, '/home/')
api.add_resource(QRCode, '/qr-code/')
api.add_resource(User, '/user/')
api.add_resource(Event, '/event/')
api.add_resource(Room, '/room/')

if __name__ == '__main__':
    # Run the app as development
    # This is modified by changing the environment var FLASK_ENV to production
    db.create_all()
    db.session.commit()
    app.run(host='0.0.0.0', debug=True, threaded=True)
