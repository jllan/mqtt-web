from mongoengine import *
import datetime
from flask_mongoengine.wtf import model_form


class Sub(Document):
    # id = Column(Integer, primary_key=True)
    address = StringField(default='127.0.0.1', required=True)
    topic = StringField(required=True)
    qoc = IntField(default=0)
    client_id = IntField()
    user_name = StringField()
    password = StringField()
    create_time = DateTimeField(default=datetime.datetime.now())

class Pub(Document):
    # id = Column(Integer, primary_key=True)
    address = StringField(default='127.0.0.1', required=True)
    topic = StringField(required=True)
    content = StringField(required=True)
    qoc = IntField(default=0)
    client_id = IntField()
    user_name = StringField()
    password = StringField()
    create_time = DateTimeField(default=datetime.datetime.now())

SubForm = model_form(Sub)
PubForm = model_form(Pub)


'''
class Sub(Model):
    __tablename__ = "sub"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    topic = Column(String(64), nullable=False)
    qoc = Column(Integer, default=0)
    client_id = Column(Integer)
    user_name = Column(String)
    password = Column(String)
    create_time = Column(DateTime, default=datetime.datetime.now())


class Pub(Model):
    __tablename__ = "pub"
    id = Column(Integer, primary_key=True)
    address = Column(String)
    topic = Column(String(64), nullable=False)
    content = Column(String(64), nullable=False)
    qoc = Column(Integer, default=0)
    client_id = Column(Integer)
    user_name = Column(String)
    password = Column(String)
    create_time = Column(DateTime, default=datetime.datetime.now())
    '''
