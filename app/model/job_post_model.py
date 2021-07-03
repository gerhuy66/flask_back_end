import re

from flask.helpers import send_file
from app.database import mysql_db
from app.database import marshmallow
# from marshmallow_sqlalchemy import ModelSchema

from marshmallow import fields
import datetime

class jpost(mysql_db.Model):
    __tablename__ = 'jpost'
    jpost_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    jpost_title = mysql_db.Column(mysql_db.String(50))
    jpost_company_nm = mysql_db.Column(mysql_db.String(50))
    jposter_nm = mysql_db.Column(mysql_db.String(50))
    salary = mysql_db.Column(mysql_db.INTEGER)
    working_place = mysql_db.Column(mysql_db.String(50))
    company_logo_url = mysql_db.Column(mysql_db.String(100))
    update_dt = mysql_db.Column(mysql_db.String(8))
    create_usr = mysql_db.Column(mysql_db.String(50))

    def create(self):
        now  = datetime.datetime.now()
        self.jpost_id ="jpost"+now.strftime("%H%M%S%m%d%Y")
        self.update_dt = now.strftime("%H%M%S%m%d%Y")
        self.create_usr = "admin"

        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self
    
    def __init__(self,jpost_title,jpost_company_nm,company_logo_url="",jposter_nm="",salary=0,working_place='vietnam'):
        self.jpost_title = jpost_title
        self.jpost_company_nm = jpost_company_nm
        self.company_logo_url = company_logo_url
        self.jposter_nm = jposter_nm
        self.salary = salary
        self.working_place = working_place
    
    def to_json(self):
        return {
            "jpost_title":self.jpost_title,
            "jpost_company_nm":self.jpost_company_nm,
            "company_logo_url":self.company_logo_url,
            "jposter_nm":self.jposter_nm,
            "salary":self.salary,
            "working_place":self.working_place,
            "update_dt":self.update_dt,
            "create_usr":self.create_usr
        }
    def __repr__(self):
        return '<jpost: %r %r>' % (self.job_name,self.job_id)

class CandidateSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = jpost
        load_instance = True
    jpost_id = fields.String(required=True)
    jpost_title = fields.String(required=True)
    jpost_company_nm = fields.String(required=True)
    jposter_nm = fields.String(required=True)
    salary = fields.String(required=True)
    working_place = fields.String(required=True)
    company_logo_url = fields.String(required=True)
    update_dt = fields.String(required=True)
    create_usr = fields.String(required=True)