from flask import Flask, request, jsonify
from flask_cors import CORS
import Extracting_Researchers
import Extracting_Funding
import json
import sys
import mysql.connector
import os
import re
import Training_Model
import Bulk_Researcher_Matcher
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

current_folder_path = str(Path(__file__).parent)

app = Flask(__name__)
CORS(app)

env_path = os.path.join(current_folder_path, '.env')

load_dotenv(env_path)

app.config["JWT_SECRET_KEY"] = os.getenv('SECRET_KEY')

jwt = JWTManager(app)

@app.route("/login", methods=['POST'])
def login():
    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    jsondata = request.json
    
    cursor = db.cursor()
    
    cursor.execute("SELECT salt FROM users WHERE username = %s", (jsondata['username'],))
    
    result = cursor.fetchall()
    
    if len(result[0]) == 1:
        encoded_password = (jsondata['password'] + result[0][0]).encode('utf-8')
        
        password = hashlib.sha512(encoded_password).hexdigest()
        
        try:
            cursor.execute("SELECT id FROM users WHERE password = %s", (password,))

            new_result = cursor.fetchone()
            
            if len(new_result) == 1:
                expires = timedelta(hours=1)

                access_token = create_access_token(identity=jsondata['username'], expires_delta=expires)
                
                return jsonify(access_token=access_token)
                
        except Exception as error:
            return 'Not Ok', 401
    
    return 'Not Ok', 401

@app.route("/researchers", methods=['POST'])
def researchers():
    jsondata = request.json
    emailpattern = "[^@]+@[^@]+\.[^@]+"
    tempemail = jsondata['email']
    if(bool(re.match(emailpattern, tempemail))):
        Extracting_Researchers.start_extraction_researchers(jsondata['profile'], jsondata['email'])
        return 'Ok'
    else:
        return "Invalid Email Format", 400
    
@app.route("/funding", methods=['POST'])
def funding():
    jsondata = request.json
    pattern = "^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"
    tempdate = jsondata['date']
    if(bool(re.match(pattern, tempdate))):
        Extracting_Funding.start_extraction_funding(jsondata['url'], jsondata['date'])
        return 'Ok'
    else:
        return "Invalid Date Format", 400

@app.route("/matchAllResearchers", methods=['GET'])
def matchAllResearchers():
    Bulk_Researcher_Matcher.match_all_researchers()
    
    return 'Ok'

@app.route("/getAllFunding", methods=['GET'])
def getAllFunding():
    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    folder_path = os.path.join(current_folder_path, "Funding_Opportunities")
    
    files = os.listdir(folder_path)

    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM funding_opportunity_urls")

    data = []
    
    for row in cursor.fetchall():
        keywords = []
        txt_file = open(os.path.join(folder_path, str(row[0]) + ".txt"), 'r', encoding="utf-8")
        txt_string = txt_file.readline()
        txt_file.close()
        keywords = txt_string.split(" ")
        keywords.pop(0)
        item = {"id": row[0], "url": row[1], "closeDate": row[2], "keywords": keywords}
        data.append(item)
    
    json_data = json.dumps(data, indent=4, default=str)
    
    return json_data
    
@app.route("/getAllResearchers", methods=['GET'])
def getAllResearchers():
    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    cursor = db.cursor()
    
    folder_path = os.path.join(current_folder_path, "Researcher_Profiles")
    
    files = os.listdir(folder_path)
    
    cursor.execute("SELECT * FROM researcher_profiles_urls")
    
    data = []
    
    for row in cursor.fetchall():
        keywords = []
        
        words = row[1].split('/')
        names = words[-1].split('-')
        formattedstring = ""  
        for name in names:
            if len(name) > 1:
                formattedstring += " " + name
        irrel_names = formattedstring
        
        txt_file = open(os.path.join(folder_path, str(row[0]) + " " + irrel_names + ".txt"), 'r', encoding="utf-8")
        txt_string = txt_file.readlines()
        txt_file.close()
        
        for line in txt_string[1:]:
            clean_line = line.rstrip('\n')
            keywords.append(clean_line)
            
        item = {"id": row[0], "url": row[1], "email": row[2], "keywords": keywords}
        data.append(item)
    
    json_data = json.dumps(data, indent=4, default=str)
    
    return json_data
    
@app.route("/getAllArchivedLinks", methods=['GET'])
def getAllArchivedLinks():
    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM archived_links");
    
    data = []
    for row in cursor.fetchall():
        item = {"id": row[0], "url": row[1], "closeDate": row[2], "reason": row[3]}
        data.append(item)
        
    json_data = json.dumps(data, indent=4, default=str)
    
    return json_data
    
@app.route("/deleteAFunding", methods=['DELETE'])
def deleteAFunding():
    jsondata = request.json
    
    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    cursor = db.cursor()
    
    id = jsondata['id']
    
    folder_path = os.path.join(current_folder_path, "Funding_Opportunities")
    
    path = os.path.join(folder_path, str(id) + ".txt")
    
    if os.path.exists(path):
        os.remove(path)
        
    try:
        try:
            cursor.execute("INSERT INTO archived_links (url, closeDate, reason) SELECT url,closeDate,'Archived' FROM funding_opportunity_urls WHERE id = %s", (str(id),))
            db.commit()
            
        except Exception as error:
            print("URL already in archived database:",error)
        
        cursor.execute("DELETE FROM funding_opportunity_urls WHERE id = %s", (str(id),))
        db.commit()
        
        Training_Model.start_training()
        
        return "Ok"
    except Exception as error:
        print(error)
    
@app.route("/deleteAResearcher", methods=['DELETE'])
def deleteAResearcher():
    jsondata = request.json

    db = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        password = os.getenv('DATABASE_PASSWORD'),
        database = os.getenv('DATABASE')
    )
    
    cursor = db.cursor()
    
    id = jsondata['id']
    url = jsondata['url']

    words = url.split('/')
    names = words[-1].split('-')
    formattedstring = ""  
    for name in names:
        if len(name) > 1:
            formattedstring += " " + name
    irrel_names = formattedstring
    
    folder_path = os.path.join(current_folder_path, "Researcher_Profiles")
    
    path = os.path.join(folder_path, str(id) + " " + irrel_names + ".txt")
    print(path)
    
    if os.path.exists(path):
        os.remove(path)
    
    try:
        cursor.execute("DELETE FROM researcher_profiles_urls WHERE id = %s", (str(id),))
        db.commit()
        
        return "Ok"
    except Exception as error:
        print(error)

if __name__ == "__main__":
    app.run()