from flask import request  # Flask, receiving data from requests, json handling
from flask import send_file  # Create url from statics files
from flask import jsonify  # Flask, receiving data from requests, json handling
from flask import after_this_request  
from flask_restful import Resource  # modules for fast creation of apis

from sqlalchemy import inspect

from config import app
from config import api
from config import db
from config import jwt
# from config import connect_to_sqlite

from functions import generate_qr_from_json
from functions import decode_qr_code

from model import Model

from typing import Any, NoReturn

from functools import wraps

from os import getcwd
from os import path 
from os import remove 

from datetime import datetime
from datetime import timedelta
from datetime import timezone


from json import loads
from json import dumps

from io import BytesIO

from time import time

from icecream import ic

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt


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

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in ('admin', 'root'):
                return fn(*args, **kwargs)
            else:
                return jsonify(status='fail', message="Admins only!")

        return decorator

    return wrapper

class Main(Resource):

    @jwt_required()
    def get(self):
        ic(model.execute('SELECT * FROM "User"'))
        return jsonify(version=API_VERSION)


class User(Resource):
    @jwt_required()
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


    # Jwt not required
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


    
    @admin_required()
    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_user(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")


class Event(Resource):

    @jwt_required()
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
            data_db['event_id'] = response
            data_db['time'] = 'begin'
            ic(dumps(data_db))
            qr_code_begin = generate_qr_from_json(data_db)
            data_db['time'] = 'end'
            qr_code_end = generate_qr_from_json(data_db)
            del data_db['time']

            try:
                begin_filename = path.join(getcwd(), f'qr_codes/{time()}.png')
                end_filename = path.join(getcwd(), f'qr_codes/{time()}.png')
                qr_code_begin.save(begin_filename, format='PNG')
                qr_code_end.save(end_filename, format='PNG')
            except Exception as e:
                return jsonify(status="fail", message="Error while inserting", log=str(e))
            model.update_event(response, qr_code_begin=begin_filename, qr_code_end=end_filename)
            data_db['qr_code_begin'] = begin_filename
            data_db['qr_code_end'] = end_filename

            return jsonify(status="good", message="Inserted correctly", 
                data=dict(event_id=response))
        else:
            return jsonify(status="fail", message="Error whil inserting")


    
    @admin_required()
    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_event(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")


class Room(Resource):

    @jwt_required()
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

    
    @admin_required()
    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_room(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")


class Assistance(Resource):
    @jwt_required()
    def get(self):
        idx = request.args.get('idx', None)
        if idx:
            response = model.read_assistance(idx)
        else:
            response = model.read_all_assistances()

        if response:
            return jsonify(status="good", message="Read correctly", 
                data=response)
        else:
            return jsonify(status="fail", message="Error whil reading")

    def post(self):
        data_db = dict(
                user_id=request.form.get("user_id", None),
                event_id=request.form.get("event_id", None),
                room_id=request.form.get("room_id", None)
            )
        if not all(data_db.values()):
            return jsonify(status="error", message="All fields are required")
        data_db['registered_end'] = None
        data_db['registered_begin'] = None
        response = model.insert_assistance(**data_db)
        if response:
            return jsonify(status="good", message="Inserted correctly", 
                data=dict(assistance_id=response))
        else:
            return jsonify(status="fail", message="Error whil inserting")


    
    @admin_required()
    def delete(self):
        idx = request.args.get('idx', None)
        response = model.delete_assistance(idx)
        if response:
            return jsonify(status="good", message="Deleted correctly")
        else:
            return jsonify(status="fail", message="Error whil deleting")

    
    @admin_required()
    def patch(self):
        qr_code = request.files.get("qr-code", None)
        data = loads(decode_qr_code(qr_code.read()))
        ic(data)
        user_id = request.args.get("user_id", None)
        state = data.get('time', None)
        if  not state:
            return jsonify(status="fail", message="Unknown code")

        if state == 'begin':
             response = model.update_assistance(int(user_id), int(data['event_id']), registered_begin=True)
             message = "Verfied at the begin"
        else:  # time == end
             response = model.update_assistance(int(user_id), int(data['event_id']), registered_end=True)
             message = "Verfied at the end"
        if response:
            return jsonify(status="good", message=message, assistance_id=response)
        else:
            return jsonify(status="fail", message="Error whil updating")


class QRCode(Resource):

    
    @admin_required()
    def get(self):

        data = dict(request.args)
        ic(data)
        try:
            qr_code = generate_qr_from_json(data)
        except Exception as e:
            return jsonify(status='error', message='Error creating code', log=str(e))

        img_byte_arr = BytesIO()
        qr_code.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return send_file(
            BytesIO(img_byte_arr),
            mimetype='image/png',
            as_attachment=True,
            attachment_filename='qr_code.png')

    @jwt_required()
    def post(self):

        qr_code = request.files.get("qr-code", None)
        if not qr_code:
            return jsonify(status='error', message='qr code not received')
        return loads(decode_qr_code(qr_code.read()))


class Calendar(Resource):

    @jwt_required()
    def post(self):
        qr_code = request.files.get('qr-code', None)

        if not qr_code:
            return jsonify(status='error', message='qr code not received')

        data = loads(decode_qr_code(qr_code.read()))
        id_room = data['id_room']

        response =  model.read_all_events_by_id_room(id_room)

        if response:
            events = []
            for event in response:
                del event['qr_code_end']
                del event['qr_code_begin']
                events.append(event)

            return jsonify(status="good", message="Read correctly", 
                data=events)
        else:
            return jsonify(status="fail", message="Error whil reading")            


class Login(Resource):

    def post(self):        
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        user = model.login(username, password)

        if user:
            additional_claims = {"role": user.user_type}  # If root, student, admin, teacher, etc
            access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=user.username, additional_claims=additional_claims)
            return jsonify(status='good', message='Login successfully', 
                data=dict(access_token=access_token, refresh_token=refresh_token))
        else:
            return jsonify(status='fail', message='wrong password or username')



api.add_resource(Main, '/home/')
api.add_resource(QRCode, '/room/qr-code/')
api.add_resource(User, '/user/')
api.add_resource(Event, '/event/')
# api.add_resource(Reservation, '/event/reserve/')
api.add_resource(Room, '/room/')
api.add_resource(Assistance, '/assistance/')
api.add_resource(Calendar, '/calendar/')
api.add_resource(Login, '/login/')




if __name__ == '__main__':
    # Run the app as development
    # This is modified by changing the environment var FLASK_ENV to production
    db.create_all()
    db.session.commit()
    app.run(host='0.0.0.0', debug=True, threaded=True)
