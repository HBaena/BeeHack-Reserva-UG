from sqlalchemy import desc, asc, text
from config import db
from typing import Union
from icecream import ic

class Model:
    """docstring for Model"""

    def __init__(self, session=db.session):
        self.__session = session

# ------------------------------------------------------------------------------------------------- #
#                                          db methods                                               #
# ------------------------------------------------------------------------------------------------- #

    def save_changes(self):
        # If there are modifica
        # tions without be added to the tables returns True
        if self.__session.dirty:
            # Update tables
            self.__session.new
        self.__session.commit()

    def undo_changes(self):
        self.__session.rollback()

    def close_session(self):
        self.__session.close()

    def execute(self, query: str, data:Union[dict, tuple]=None):
        query = text(query)
        response = self.__session.execute(query)
        return response.fetchall()

    """
        USER METHODS
    """
    def insert_user(self, 
        username, full_name, 
        password, email, 
        user_type, career,
        division):
        try:
            new_user = User(username=username, full_name=full_name, 
                password=password, email=email, 
                user_type=user_type, career=career,
                division=division)
            self.__session.add(new_user)
            self.__session.commit()
            self.__session.refresh(new_user)
            return new_user.user_id
        except Exception as e:
            return None

    def read_user(self, user_id):
        try:
            return User.query.get(user_id).to_dict()
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None


    def read_all_users(self):
        try:
            return list(map(lambda row: row.to_dict(), User.query.all()))
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None

    def delete_user(self, user_id):
        try:
            response = User.query.filter_by(user_id=user_id).delete()
            self.__session.commit()
            return response
        except Exception as e:
            ic(e)
            return None

    """
        Event METHODS
    """
    def insert_event(self,
            name=None, description=None, topic=None, hour_begin=None, 
            duration=None, speaker=None, credits=None, credit_type=None, qr_code_begin=None, 
            qr_code_end=None, room_id=None, user_id=None):
        try:
            new_event = Event(
                name, description, topic, hour_begin, 
                duration, speaker, credits, credit_type, qr_code_begin, 
                qr_code_end, room_id, user_id)
            self.__session.add(new_event)
            self.__session.commit()
            self.__session.refresh(new_event)
            return new_event.event_id
        except Exception as e:
            ic(e)
            return None

    def read_event(self, event_id):
        try:
            return Event.query.get(event_id).to_dict()
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None


    def read_all_events(self):
        try:
            return list(map(lambda row: row.to_dict(), Event.query.all()))
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None

    def delete_event(self, event_id):
        try:
            response = Event.query.filter_by(event_id=user_id).delete()
            self.__session.commit()
            return response
        except Exception as e:
            ic(e)
            return None



    """
        ROOM METHODS
    """
    def insert_room(self, size=None,name=None,description=None,
            building=None,division=None,campus=None):
        try:
            new_room = Room(size=size,name=name,description=description,
            building=building,division=division,campus=campus)
            self.__session.add(new_room)
            self.__session.commit()
            self.__session.refresh(new_room)
            return new_room.room_id
        except Exception as e:
            ic(e)
            return None

    def read_room(self, room_id):
        try:
            return Room.query.get(room_id).to_dict()
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None


    def read_all_rooms(self):
        try:
            return list(map(lambda row: row.to_dict(), Room.query.all()))
            # return self.__session.query(User).filter(user_id).first().to_dict()
        except Exception as e:
            ic(e)
            return None

    def delete_room(self, room_id):
        try:
            response = Room.query.filter_by(room_id=room_id).delete()
            self.__session.commit()
            return response
        except Exception as e:
            ic(e)
            return None




class User(db.Model):
    __tablename__ = "User"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    user_type = db.Column(db.String(30), nullable=False)
    career = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return dict(
            user_id=self.user_id, username=self.username,
            full_name=self.full_name, password=self.password,
            email=self.email, user_type=self.user_type,
            career=self.career, division=self.division
            )
    # 1 - M
    assistance = db.relationship('Assistance', backref='User', cascade='all, delete-orphan')
    event = db.relationship('Event', backref='User', cascade='all, delete-orphan')


class Event(db.Model):

    __tablename__ = "Event" 

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True, default=None)
    topic = db.Column(db.String(40), nullable=True, default=None)

    hour_begin = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    speaker = db.Column(db.String(100), nullable=True, default=None)
    credits = db.Column(db.Float, nullable=True, default=None)
    credit_type = db.Column(db.Float, nullable=True, default=None)

    qr_code_begin = db.Column(db.String(50), nullable=True, default=None)
    qr_code_end = db.Column(db.String(50), nullable=True, default=None)


    # M - 1
    room_id = db.Column(db.Integer, db.ForeignKey("Room.room_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)


    # 1 - M
    assistance = db.relationship('Assistance', backref='Event', cascade='all, delete-orphan')


    def to_dict(self):
        return dict(
            event_id=self.event_id, name=self.name,
            description=self.description, topic=self.topic,
            hour_begin=self.hour_begin, duration=self.duration,
            speaker=self.speaker, credits=self.credits,
            credit_type=self.credit_type, qr_code_begin=self.qr_code_begin,
            qr_code_end=self.qr_code_end, room_id=self.room_id,
            user_id=self.user_id,
            )

class Room(db.Model):

    __tablename__ = "Room" 

    room_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=True, default=None)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True, default=None)

    building = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(100), nullable=False)
    campus = db.Column(db.String(50), nullable=False)



    # 1 - M
    event = db.relationship('Event', backref='Room', cascade='all, delete-orphan')

    def to_dict(self):
        return dict(
            room_id=self.room_id,
            size=self.size,
            name=self.name,
            description=self.description,
            building=self.building,
            division=self.division,
            campus=self.campus,
            )

class Assistance(db.Model):
    __tablename__ = "Assistance"


    assistance_id = db.Column(db.Integer, primary_key=True)

    registered_begin = db.Column(db.Boolean, nullable=True, default=False)
    registered_end = db.Column(db.Boolean, nullable=True, default=False)

    # M - 1
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("Event.event_id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("Room.room_id"), nullable=False)

