import os 
import json 
from flask import Flask, request, jsonify
from pathlib import Path
from werkzeug.utils import secure_filename
from preprocessorSDWAN import load_data, parse_data
import requests 
 
app = Flask(__name__)
 
# yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml") 

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'yaml', 'yml'])
 
loaded_data = {}  

# 7/5: from Ruben's code
def allowed_file(filename):
    # 7/5:  This returns the file extension.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
 
# This function will take all that "file upload" malarkey, then process
@app.route('/from-gui', methods=['GET','POST'])
def fromgui(): 
    if request.method == 'POST': 
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        # Attempt to grab the yaml file
        file = request.files['file'] 
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading.'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            file = request.files['file']
            # !! 7/5:  How do I check if this was successful? 
            raw_yaml_data = file.stream.read()
            file.stream.close() 
            resp = jsonify({'message': 'file successfully read'})
            resp.status_code = 201

 
            # ? Do I have to make raw_yaml_file into json.loads before I send
            # !! this should probably be a function imported from the sdwan preprocessor eventually

            processed_yaml = json.loads(raw_yaml_data)

            url = 'http://127.0.0.1:8000/from-preprocessor'

            # eventually also define non-yaml data here, with requests.form? 
 
            payload = {
                'yaml_data' : processed_yaml

            }
            # 7-5: json=payload added. !!actual sending is as a json string file.
            requests.post(url, json=payload)
            return resp
        else: 
            resp = jsonify({'message': 'Allowed file types are txt pdf png jpg yaml etc'})
            resp.status_code = 400
            return resp
'''
    if request.method == 'GET': 
        # 6/30: Temporary for bugchecking.
        if not raw_yaml_data:
            return "Woops, your initial POST request didn't work."
        else:
            return raw_yaml_data
'''

 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)