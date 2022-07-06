
import json 
from flask import Flask, request, jsonify
# these functions will be incorporated when refactoring 
from preprocessorSDWAN import load_data, parse_data
import requests 
import yaml

app = Flask(__name__)
  

ALLOWED_EXTENSIONS = set(['yaml', 'yml'])

# needed?  
payload2 = {}

 
def allowed_file(filename):
    # 7/5:  This is just going to return the file extension.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
  
@app.route('/from-gui', methods=['GET','POST'])
def fromgui(): 
    # 7/6 : see what happens when we save request.json as Ruben suggested
    # 7/6, later:  We can't, because it's not being sent from the gui as a json file 
    if request.method == 'POST': 
        if 'file' not in request.files:
            resp = jsonify({'Failure': 'No "File" key in the request'})
            resp.status_code = 400
            return resp     
        # Attempt to grab the yaml file
        file = request.files['file'] 
        if file.filename == '':
            resp = jsonify({'Failure': 'No file selected for uploading.'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename): 
            # 7/5 8:31pm:  This is probably where the actual problem lies. 
            file = request.files['file']
            raw_yaml_data = file.stream.read()
            file.stream.close()
            #  could add the filename for pizazz
            resp = jsonify({'Success': 'File successfully read'})
            resp.status_code = 201


            processed_yaml = yaml.safe_load(raw_yaml_data)

            payload2['yaml_data'] = processed_yaml
            payload2['product'] = request.form['product']
            
            # reminder that you need to make the boolean value here a string, actually, before you send.
            if request.form['gdoc_type'] == True:
                payload2['gdoc_type'] == "True"
            else:
                payload2['gdoc_type'] = "False"
             
            url = 'http://127.0.0.1:8000/from-preprocessor'
                 
     
            # 7-5: json=payload added. !! actual sending is as a json string file.
            requests.post(url, json=payload2)
            return payload2['gdoc_type']
        else: 
            resp = jsonify({'Failure': 'File type must be yaml/yaml'})
            resp.status_code = 400
            return resp 

# 7/6: This can likely be removed, but keeping it for bugfixing purposes for now.
    if request.method == 'GET':
        exists = 'payload2' in locals() or 'payload2' in globals()

        if not exists:
            return "Woops, your initial POST request didn't work."
        else:
            return payload2

 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)