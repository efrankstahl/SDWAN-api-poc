# 7/6 : this version correctly returns the processed yaml file as part of a paylaod. 

import os 
import json 
from flask import Flask, request, jsonify
from pathlib import Path 
# these functions will be incorporated when refactoring 
from preprocessorSDWAN import load_data, parse_data
import requests 
import yaml

app = Flask(__name__)
  

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'yaml', 'yml'])

# needed? 
loaded_data = {} 


# 7/5: from Ruben's code
def allowed_file(filename):
    # 7/5:  This is just going to return the file extension.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
 
# This function will take all that "file upload" malarkey, then process
@app.route('/from-gui', methods=['GET','POST'])
def fromgui(): 
    # 7/6 : see what happens when we save request.json as Ruben suggested
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
            # 7/5 8:31pm:  This is probably where the actual problem lies. 
            file = request.files['file']
            raw_yaml_data = file.stream.read()
            file.stream.close()
            #  could add the filename for pizazz
            resp = jsonify({'message': 'file successfully read'})
            resp.status_code = 201

            # 7/6 2:45pm:  this is necessary in templating engine... is it necessary here?
            ''' 
            raw_incoming = request.json
            if raw_incoming['gdoc_type'] == True:
                type_string = "True"
            else:
                type_string = "False"
            '''
            processed_yaml = yaml.safe_load(raw_yaml_data)

            url = 'http://127.0.0.1:8000/from-preprocessor'
            
            # will eventually have to parse non-file data too.. via requests.form?
            
            # Define payload here: 
            payload2 = {
                'yaml_data' : processed_yaml,

            }
            '''
                            'product' : raw_incoming['product'],
                'gdoc_type' : type_string
                 
                 
                 '''
            # 7-5: json=payload added. !!actual sending is as a json string file.
            requests.post(url, json=payload2)
            return payload2
        else: 
            resp = jsonify({'message': 'Allowed file types are txt pdf png jpg yaml etc'})
            resp.status_code = 400
            return resp 
    if request.method == 'GET':
        exists = 'payload2' in locals() or 'payload2' in globals()

        if not exists:
            return "Woops, your initial POST request didn't work."
        else:
            return payload2

 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)