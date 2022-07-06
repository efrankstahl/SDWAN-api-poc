
import json 
from flask import Flask, request 
from pathlib import Path
from preprocessorSDWAN import load_data, parse_data
import requests 
 
app = Flask(__name__)

# 7/1:  The payload from the api POST is going to contain the extra info, like product
#     ! The actual config data will be sent as an uploaded file.   
# yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml") 

# needed? 
loaded_data = {} 

# 7/5: from Ruben's code
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine."
 
# This function will take all that "file upload" malarkey, then process
@app.route('/from-gui', methods=['GET','POST'])
def fromgui():
    if request.method == 'POST':
        # 7/5:  Do we use request.incoming like we did in the preproc? 
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

         
        
        # 7-5: json=payload added. actual sendnig is as a json string file.
        requests.post(url, json=payload)
        return "Data submitted."
    if request.method == 'GET': 
        # 6/30: Temporary for bugchecking.
        if not loaded_data:
            return "Woops, your initial POST request didn't work."
        else:
            return loaded_data['raw_data'] 
 

 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)