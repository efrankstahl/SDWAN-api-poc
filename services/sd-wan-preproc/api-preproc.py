
import json 
from flask import Flask, request, jsonify
# TODO: Just put parse_data() in this app.
from preprocessorSDWAN import parse_data
import logging
import requests 
import sys
import yaml


app = Flask(__name__)

"""
Logger initialization
"""

tag = {'app_name': 'SDWAN Preprocessor'}
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('services\sd-wan-preproc\SDWAN-preprocessor-log.txt')
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - [ %(app_name)s ] -  %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

logger = logging.LoggerAdapter(logger, tag)




ALLOWED_EXTENSIONS = set(['yaml', 'yml'])

# Test if necessary.  
payload2 = {}

 
def allowed_file(filename):
    # 7/5:  This is just going to return the file extension.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
  

@app.route('/sdwan-preprocessor', methods=['POST'])
def fromgui(): 
    # 7/6 : see what happens when we save request.json as Ruben suggested
    # 7/6, later:  We can't, because it's not being sent from the gui as a json file 
    # TODO: Try/except.  But low priority.
    if request.method == 'POST': 
        logger.info('POST request received.')
        if 'file' not in request.files:
            resp = jsonify({'Failure': 'Request does not contain "File" key.'})
            resp.status_code = 400
            logger.critical("yaml upload failed; request didn't contain 'file' key.")
            return resp     
        # Attempt to grab the yaml file:
        file = request.files['file'] 
        if file.filename == '':
            resp = jsonify({'Failure': 'No file selected for uploading.'})
            resp.status_code = 400
            logger.critical("yaml upload failed; no value in 'file' key")
            return resp
        # Success case:
        if file and allowed_file(file.filename): 
            logger.info('yaml file succesfully received.')
            file = request.files['file']
            raw_yaml_data = file.stream.read()
            file.stream.close()
            #  Add filename? 
            resp = jsonify({'Success': 'File successfully read'})
            resp.status_code = 201

            processed_yaml = yaml.safe_load(raw_yaml_data)
            parsed_data = parse_data(processed_yaml)

            # Craft post request for template engine.
            payload2['parsed_data'] = parsed_data
            payload2['product'] = request.form['product']
            payload2['doc_name'] = request.form['doc_name']
            payload2['init_id'] = request.form['init_id']
            # TODO:  Ruben says send as string, Robert says Boolean.
            if request.form['gdoc_type'] == True:
                payload2['gdoc_type'] == "True"
            else:
                payload2['gdoc_type'] = "False"


             
            url = 'http://127.0.0.1:8000/templating-engine'
                 
     
            # Send payload as json.
            # TODO: Is there a way to check it was succsesfully sent?
            requests.post(url, json=payload2)
            return resp
        else: 
            resp = jsonify({'Failure': 'File type must be yaml/yaml'})
            resp.status_code = 400
           # logging.critical("yaml upload failed; bad file type")
            return resp 
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)