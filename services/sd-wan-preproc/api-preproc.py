
import json 
from flask import Flask, request 
from pathlib import Path
from preprocessorSDWAN import load_data, parse_data
import requests 
 
app = Flask(__name__)

# 7/1:  The payload from the api POST is going to contain the extra info, like product
#     ! The actual config data will be sent as an uploaded file.  

# 6/28: Will import an API file upload eventually, but will have to figure out how from scratch. 
yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml") 
sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_v3.jinja2")

loaded_data = {} 

@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
 
# This function will take all that "file upload" malarkey, then process
@app.route('/from-gui', methods=['GET','POST'])
def fromgui():
    if request.method == 'POST':
        # PLACEHOLDER.  This data will be sent by the gui as a file upload.
        loaded_data['raw_data'] = load_data(yaml_raw)
        # Below data is supplied by gui as a payload
        loaded_data['product'] = request.form['product'] 
        loaded_data['replacement_values'] = request.form['replacement_values']
        loaded_data['gdoc_type'] = request.form['gdoc_type']

        # 6:29: going to exclude this for now to remove unncessary compelxity 
        # parsed_data = parse_data(loaded_data['raw_data']) 

        # Anton 6/28:  the data that gets 'returned' is used by the next method in the process. 
        #               ? how to write it so that 'return' delivers that?
    
        # 7/1 - what about the non-config data?  does loaded_data process a dict ok?
        payload = loaded_data

        # 6/29: processing the post request (or whatever) from the GUI
        # now triggers a post request to the template engine
        url = 'http://127.0.0.1:8000/from-preprocessor'

         
        
    
        requests.post(url, data=payload)
        return "Data submitted."
    if request.method == 'GET': 
        # 6/30: Temporary for bugchecking.
        if not loaded_data:
            return "Woops, your initial POST request didn't work."
        else:
            return loaded_data 
 

 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)