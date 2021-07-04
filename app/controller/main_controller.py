from flask import json, render_template, request, session, \
Response,jsonify,redirect,url_for,flash,make_response,Flask,send_file,send_from_directory
from app import app
from app.service.elastic import es
from app.service.haystack import cv_search_haystack

@app.route("/",methods=['GET'])
def home():
    return render_template("search_page.html")

@app.route("/searchCV",methods=['POST'])
def search_cv():
    searFil = request.json['searchFilter']
    searVal = request.json['searchVal']
    body = {
    "from":0,
    "size":100,
    "query": {
        "bool": {
          "should": [
            {
              "match": {
                searFil: searVal
                }
            }
            ]
            }
        }
    }
    res = es.search(index="cv", body=body)
    print(res)
    return make_response(jsonify({"res":res['hits']['hits']}))

@app.route("/searchCvAdvance",methods=['POST'])
def search_advance():
    # searchVals = request.json['searchDict']
    conditions = []
    for key in request.json.keys():
        conditions.append({"match":{key:request.json[key]}})
    body = {
    "from":0,
    "size":100,
    "query": {
        "bool": {
          "should": conditions
            }
        }
    }
    res = es.search(index="cv", body=body)
    print(res)
    return make_response(jsonify({"res":res['hits']['hits']}))


@app.route("/haystack",methods=['GET','POST'])
def haystack_search():
    query = "sinh viên"
    try:
       query = request.json['haystackData']
    except:
        print("haystackData null")
    res = cv_search_haystack.search_cv(query)
    return make_response(jsonify({'status':200,'result':res}))
    
import os
@app.route('/download/<pdffile>',methods=['GET','POST'])
def download_file(pdffile):
    current_dir = os.getcwd()
    # path = request.json['filename']
    # path = os.path.join(os.getcwdb(), "\\CV_PDF\\"+filename)
    uploads = os.path.join(app.root_path.replace("\\app",""), "CV_PDF")
    uploads = os.path.join(uploads,pdffile)
    return send_file(uploads, as_attachment=True)

@app.route('/getAllDocuments/<index>/<doctype>/<infrom>/<size>',methods=['get'])
def getAllDocuments(index,doctype,infrom,size):

    res = es.search(index=index, doc_type=doctype, body={"from":infrom,
    "size":size,'query':{"match_all":{}} })

    respon = {
        "total_doc" : res['hits']['total']['value'],
        "documents" : res['hits']['hits']
    }
    return make_response(jsonify({"status":200,"result":respon}))

@app.route('/deleteDocument',methods=['post'])
def deleteDocument():
    doc_id = request.json['docId']
    try:
        es.delete(index="cv",doc_type="cv",id=doc_id)
    except:
        return make_response(jsonify({'status':200,'result':{"deleted":"fail","message":"delete fail!"}}))
    return make_response(jsonify({'status':200,'result':{"deleted":"success","message":"delete successfull!"}}))

@app.route('/searchText',methods=['GET','POST'])
def searchText():
    query = "sinh viên"
    try:
       query = request.json['haystackData']
    except:
        print("haystackData null")

    res = cv_search_haystack.search_document(query)
    return make_response(jsonify({'status':200,'result':res}))


@app.route('/addDocument',methods=['post'])
def addDocument():
    return ""


@app.route('/getImage/<imageNm>',methods=['GET'])
def get_image(imageNm):
    current_dir = os.getcwd()
    # path = request.json['filename']
    # path = os.path.join(os.getcwdb(), "\\CV_PDF\\"+filename)
    uploads = os.path.join(app.root_path.replace("\\app",""), "CV_IMG")
    uploads = os.path.join(uploads,imageNm)
    return send_file(uploads, mimetype='image/jpg')