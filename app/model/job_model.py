import re

from flask.helpers import send_file
from app.database import mysql_db
from app.database import marshmallow
# from marshmallow_sqlalchemy import ModelSchema

from marshmallow import fields
import datetime

class job(mysql_db.Model):
    __tablename__ = 'job'
    job_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    job_name = mysql_db.Column(mysql_db.String(50))
    update_dt = mysql_db.Column(mysql_db.String(8))
    create_usr = mysql_db.Column(mysql_db.String(50))

    def create(self):
        now  = datetime.datetime.now()
        self.job_id ="cv"+now.strftime("%H%M%S%m%d%Y")
        self.update_dt = now.strftime("%H%M%S%m%d%Y")
        self.create_usr = "admin"
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self
    
    def __init__(self,job_name):
        self.job_name = job_name
    
    def to_json(self):
        return {
            "job_name":self.job_name,
        }
    def __repr__(self):
        return '<Job: %r %r>' % (self.job_name,self.job_id)

class CandidateSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = job
        load_instance = True
    job_id = fields.String(required=True)
    job_name = fields.String(required=True)
    update_dt = fields.String(required=True)
    create_usr = fields.String(required=True)