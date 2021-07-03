import flask
from flask import json, render_template, request, session, Response,jsonify,redirect,url_for,flash,make_response,Flask
# from flask_jobs import JobScheduler
import datetime
import time
# from flask_s3 import FlaskS3
from flask_cors import CORS, cross_origin


app = Flask(__name__,static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from app.model import cv_model,candidate_mode,job_model,job_post_model
# s3 = FlaskS3(app)
# app.static_url_path ='https://cvsearchwebstorage.s3.ap-southeast-1.amazonaws.com/'
# app.debug = True

from app.controller import main_controller

from app.database import mysql_db
# from app.service.selenium import get_link_linkedin
# mysql_db.create_all()

# from app.service import scheduled_job
# scheduled_job.create_repeat_job()














@app.shell_context_processor
def make_shell_context():
    return dict(db=mysql_db)