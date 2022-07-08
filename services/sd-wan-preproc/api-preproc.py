
import json 
from flask import Flask, request, jsonify
# Will potentially incorporate the below when refactoring:   
# from preprocessorSDWAN import load_data, parse_data
import logging
import requests 
import sys
import yaml


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s -  %(levelname)s -  %(message)s')  

ALLOWED_EXTENSIONS = set(['yaml', 'yml'])

# Test if necessary.  
payload2 = {}

 
def allowed_file(filename):
    # 7/5:  This is just going to return the file extension.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
  
@app.route('/from-gui', methods=['POST'])
def fromgui(): 
    # 7/6 : see what happens when we save request.json as Ruben suggested
    # 7/6, later:  We can't, because it's not being sent from the gui as a json file 
    if request.method == 'POST': 
        if 'file' not in request.files:
            resp = jsonify({'Failure': 'Request does not contain "File" key.'})
            resp.status_code = 400
            return resp     
        # Attempt to grab the yaml file:
        file = request.files['file'] 
        if file.filename == '':
            resp = jsonify({'Failure': 'No file selected for uploading.'})
            resp.status_code = 400
            return resp
        # Success case:
        if file and allowed_file(file.filename): 
            file = request.files['file']
            raw_yaml_data = file.stream.read()
            file.stream.close()
            #  Add filename? 
            resp = jsonify({'Success': 'File successfully read'})
            resp.status_code = 201


            processed_yaml = yaml.safe_load(raw_yaml_data)

            # Craft post request for template engine.
            payload2['yaml_data'] = processed_yaml
            payload2['product'] = request.form['product']
            payload2['doc_name'] = request.form['doc_name']
            payload2['init_id'] = request.form['init_id']
            # Convert Boolean to string before sending.
            if request.form['gdoc_type'] == True:
                payload2['gdoc_type'] == "True"
            else:
                payload2['gdoc_type'] = "False"


             
            url = 'http://127.0.0.1:8000/from-preprocessor'
                 
     
            # Send payload as json.
            requests.post(url, json=payload2)
            return resp
        else: 
            resp = jsonify({'Failure': 'File type must be yaml/yaml'})
            resp.status_code = 400
            return resp 
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)