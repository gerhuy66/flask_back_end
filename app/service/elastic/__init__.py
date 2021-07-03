from elasticsearch import Elasticsearch,RequestsHttpConnection
from requests_aws4auth import AWS4Auth
service = 'es'
access_key = 'AKIAXYZRVWASFJT4DGP7'
serect_key = '0aZ9MB6OIiELdf4JJQ61Z4cg8MXo3yBlPGKm+9RR'
region = 'ap-southeast-1'
awsauth = AWS4Auth(access_key, serect_key,region,service)


es = Elasticsearch(["https://search-cvsearch-2hgyzv2t5gdogt27c3ehhxrxku.ap-southeast-1.es.amazonaws.com:443"],http_auth = awsauth,use_ssl = True,verify_certs = True,connection_class = RequestsHttpConnection,request_timeout = 30)
