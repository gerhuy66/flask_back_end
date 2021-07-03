from os import path
from haystack.reader.farm import FARMReader
from app import app as app_context
# from flask_s3 import FlaskS3
# import boto3
# import flask
# elastic_host = "localhost"
model_path = app_context.root_path+"\\service\\haystack\\bert-multi-cased-finetuned-xquadv1"


from requests_aws4auth import AWS4Auth
service = 'es'
access_key = ''
serect_key = ''
region = 'ap-southeast-1'
awsauth = AWS4Auth(access_key, serect_key,region,service)


farm_reader = FARMReader(model_name_or_path = model_path,use_gpu=False,num_processes=1)
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

document_store = ElasticsearchDocumentStore(host="search-cvsearch-2hgyzv2t5gdogt27c3ehhxrxku.ap-southeast-1.es.amazonaws.com",port=443, aws4auth = awsauth,username="admin", password="", scheme='https',index="document",embedding_field=None)
