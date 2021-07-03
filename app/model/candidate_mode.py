from enum import Enum
import re

from flask.helpers import send_file
from app.database import mysql_db
from app.database import marshmallow
# from marshmallow_sqlalchemy import ModelSchema

from marshmallow import fields
import datetime

class candidate(mysql_db.Model):
    __tablename__ = 'candidate'
    can_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    can_name = mysql_db.Column(mysql_db.String(50))
    can_major = mysql_db.Column(mysql_db.String(50))
    can_age = mysql_db.Column(mysql_db.String(50))
    can_gender = mysql_db.Column(mysql_db.String(1))
    can_hobby = mysql_db.Column(mysql_db.String(50))
    can_birthdate = mysql_db.Column(mysql_db.String(50))
    update_dt = mysql_db.Column(mysql_db.String(8))
    create_usr = mysql_db.Column(mysql_db.String(50))

    def create(self):
        now  = datetime.datetime.now()
        self.can_id ="can"+now.strftime("%H%M%S%m%d%Y")
        self.update_dt = now.strftime("%H%M%S%m%d%Y")
        self.create_usr = "admin"
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self
    
    def __init__(self,can_name,can_major,can_age,can_gender,can_hobby,can_birthdate):
        self.can_name = can_name
        self.can_major = can_major
        self.can_age = can_age
        self.can_gender = can_gender
        self.can_hobby = can_hobby
        self.can_birthdate = can_birthdate
    
    def to_json(self):
        return {
            "can_name":self.can_name,
            "can_major": self.can_major,
            "can_age": self.can_age,
            "can_hobby" : self.can_hobby,
            "can_gender" : self.can_gender,
            "can_birthdate":self.can_birthdate,
            "update_dt" : self.update_dt,
            "create_usr":self.create_usr
        }
    def __repr__(self):
        return '<Candidate: %r %r>' % (self.can_name,self.can_major)

class CandidateSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = candidate
        load_instance = True
    can_id = fields.String(required=True)
    can_name = fields.String(required=True)
    can_major = fields.String(required=True)
    can_gender = fields.String(required=True)
    can_age = fields.String(required=True)
    can_hobby = fields.String(required=True)
    update_dt = fields.String(required=True)
    create_usr = fields.String(required=True)

        