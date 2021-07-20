from elasticsearch import Elasticsearch,RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from tika import parser
import io

service = 'es'
access_key = 'AKIAXYZRVWASFJT4DGP7'
serect_key = '0aZ9MB6OIiELdf4JJQ61Z4cg8MXo3yBlPGKm+9RR'
region = 'ap-southeast-1'
awsauth = AWS4Auth(access_key, serect_key,region,service)
import datetime

es = Elasticsearch(["https://search-cvsearch-2hgyzv2t5gdogt27c3ehhxrxku.ap-southeast-1.es.amazonaws.com:443"],http_auth = awsauth,use_ssl = True,verify_certs = True,connection_class = RequestsHttpConnection,request_timeout = 30,timeout=30)
import regex as re
def convert_elastic(file):
    print(file)
    f = open(file, encoding="utf-8",errors='replace')
    lines = f.readlines()
    vn_last_name = ["nguyễn","trần","võ","huỳnh","đặng","lê","phạm","huỳnh","hoàng","đỗ","phan","ngô","dương","lý","vũ"]
    cv_profile = {}
    cv_profile["cv_content"] = ""
    cv_profile["file_name"] = file.split("/")[1]
    for i in range(len(lines)):
        cv_profile["cv_content"] = cv_profile["cv_content"]+lines[i]
        lines[i] = lines[i].lower()
        #get name
        if lines[i].split(" ")[0] in vn_last_name:
            if "full_name" not in cv_profile:
                cv_profile["full_name"] = lines[i]
        #get birth date
        if "birth_date" not in cv_profile:
            match = re.search(r'\d{2}/\d{2}/\d{4}', lines[i])
            if match != None:
                cv_profile["birth_date"] = datetime.datetime.strptime(match.group(), '%d/%m/%Y').strftime("%d/%m/%Y")
            else:
                match1 = re.search(r'\d{4}/\d{2}/\d{2}', lines[i])
                if match1 != None:
                    try:
                        cv_profile["birth_date"] = datetime.datetime.strptime(match1.group(), '%Y/%d/%m').strftime("%d/%m/%Y")
                    except:
                        cv_profile["birth_date"] = ""
        #get email
        if "email" not in cv_profile:
            match = re.search(r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', lines[i])
            if match:
                cv_profile["email"] = match.group()
                print(match.group())
        #get phone number
        if re.search(r'[0-9]{1}[0-9]{9,13}$', lines[i]) != None:
            if "phone" not in cv_profile:
                cv_profile["phone"] = re.search(r'[0-9]{1}[0-9]{3,13}$', lines[i]).group()
        
        if 'phone' in lines[i] or 'điện thoại' in lines[i]:
            try:
                value = lines[i].split("phone")[1].strip()
                if re.match(r'[0-9]*',value.replace('+84','0')).group(0) != '':
                    cv_profile["phone"] = value
            except:
                value = lines[i].split("điện thoại")[1].strip()
                if re.match(r'[0-9]*',value.replace('+84','0')).group(0) != '':
                    cv_profile["điện thoại"] = value
        #Get address
        if "địa chỉ" in lines[i] or "address" in lines[i]:
            if "address" not in cv_profile:
                try:
                    cv_profile["address"] = lines[i].split("address")[1].strip()
                except:
                    cv_profile["address"] = lines[i+1]
            if "address" not in cv_profile:
                try:
                    cv_profile["address"] = lines[i].split("địa chỉ")[1].strip()
                except:
                    cv_profile["address"] = lines[i+1]
        #get gender
        if "giới tính" in lines[i] or "gender" in lines[i]:
            print(lines[i])
            if "gender" not in cv_profile:
                try:
                    cv_profile["gender"] = lines[i].split("gender")[1].strip()
                except:
                    cv_profile["gender"] = lines[i+1]
            if "gender" not in cv_profile:
                try:
                    cv_profile["gender"] = lines[i].split("giới tính")[1].strip()
                except:
                    cv_profile["gender"] = lines[i+1]
        if 'nam' in lines[i] and "gender" not in cv_profile:
            cv_profile["gender"] = 'Nam'
        if 'nữ' in lines[i] and "gender" not in cv_profile:
            cv_profile["gender"] = 'Nữ'
        #get major
        if "nghành" in lines[i] or "major" in lines[i] or "khoa" in lines[i]:
            if "major" not in cv_profile:
                cv_profile["major"] = lines[i].replace("nghành","").replace("major","").replace(':','').replace("khoa","")
        # get language
        if "tiếng" in lines[i] or "language" in lines[i] or "ngoại ngữ" in lines[i]:
            value = lines[i].replace("ngoại ngữ","").replace("language","").replace(':','')
            if "language" not in cv_profile:
                cv_profile["language"] = value
            else:
                cv_profile["language"] = cv_profile["language"] + ", " + value
                
        if "mong muốn" in lines[i]:
            if "target" not in cv_profile:
                cv_profile["target"] = lines[i].replace("mong muốn","").replace(':','')
            else:
                cv_profile["target"] = cv_profile["target"] + lines[i].replace("mong muốn","").replace(':','')
        if "vị trí" in lines [i]:
            if "old_position" not in cv_profile:
                cv_profile['old_position'] = lines[i].replace("vị trí","").replace(':','')
        if "kỹ năng" in lines[i] or "khả năng" in lines[i] or "skill" in lines[i]:
            value = lines[i].replace("kỹ năng","").replace(':','')
            if "skills" not in cv_profile:
                cv_profile['skills'] = value
            else:
                cv_profile['skills'] = cv_profile['skills'] + value
    f.close()
    print("==============================================================="+"\n")
    for key in cv_profile.keys():
        if key != 'cv_content':
            print(key+":" + cv_profile[key].replace('\n',' ')+'\n')
    print("==============================================================="+"\n")

    return cv_profile
import os

def checkValidFile(filename):
    if filename.find("(1)") != -1 \
    or filename.find("(2)") != -1 \
    or filename.find("(3)") != -1 \
    or filename.find("(4)") != -1 \
    or filename.find("(5)") != -1 \
    or filename.find("(6)") != -1 \
    or filename.find("(7)") != -1 \
    or filename.find("(8)") != -1 \
    or filename.find("(9)") != -1 \
    or filename.find("(10)") != -1:
        return False 
    else:
        return True


def pdf2text(pdf_dir = "uploadhandle",ouput_dir = "uploadhandleText"):
    f = os.listdir(pdf_dir)
    ignore = ("cv_timviec_ten-ung-vien")
    for f1 in f:
        if ignore in f1:
            break
        try:
            raw = parser.from_file(pdf_dir + '/' + f1)
            txtFile = open(ouput_dir + '/' + f1.replace('.pdf','.txt'),'w', encoding="utf8")
            txtFile.write(re.sub(r"\n+", "\n", raw['content']))
            txtFile.close()
        except:
            print(f1)
    print("convert Done")

def index_elastic(text_dir = 'uploadhandleText'):
    f = os.listdir(text_dir)
    count = 0
    indexed_docs = []
    for i in range(len(f)):
        if checkValidFile(f[i]) == False:
            continue
        temp = convert_elastic(text_dir + '/' + f[i])
        es.index(index="cv",doc_type="cv",id=i,body=temp)
        indexed_docs.append(temp)
        count += 1
    print("total indeces: "+str(count))
    
    return {"docs":indexed_docs,"totals":str(count)}