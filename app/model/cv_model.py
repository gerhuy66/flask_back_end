import re
from app.database import mysql_db
from app.database import marshmallow
# from marshmallow_sqlalchemy import ModelSchema

from marshmallow import fields
import datetime

class CV(mysql_db.Model):
    __tablename__ = 'cv'
    cv_id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    cv_type = mysql_db.Column(mysql_db.String(50))
    text_url = mysql_db.Column(mysql_db.String(50))
    pdf_url = mysql_db.Column(mysql_db.String(50))
    update_dt = mysql_db.Column(mysql_db.String(8))
    create_usr = mysql_db.Column(mysql_db.String(50))

    def create(self):
        now  = datetime.datetime.now()
        self.cv_id ="cv"+now.strftime("%H%M%S%m%d%Y")
        self.update_dt = now.strftime("%H%M%S%m%d%Y")
        self.create_usr = "admin"
        mysql_db.session.add(self)
        mysql_db.session.commit()
        return self
    
    def __init__(self,cv_type,text_url,pdf_url):
        self.cv_type = cv_type
        self.text_url = text_url
        self.pdf_url = pdf_url
    
    def to_json(self):
        return {
            "cv_id":self.cv_id,
            "cv_type": self.cv_type,
            "text_url": self.text_url,
            "pdf_url" : self.pdf_url,
            "update_dt":self.update_dt
        }
    def __repr__(self):
        return '<CV: %r %r %r %r>' % (self.cv_id,self.cv_type,self.text_url,self.pdf_url)

class CvSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = CV
        load_instance = True
    cv_id = fields.String(required=True)
    cv_type = fields.String(required=True)
    text_url = fields.String(required=True)
    pdf_url = fields.String(required=True)
    update_dt = fields.String(required=True)
    create_usr = fields.String(required=True)

        