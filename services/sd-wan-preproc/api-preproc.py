# 6/28 - as-yet unchanged from the original draft
# 6/29: THIS IS BROKEN, it gives an ENOROMOUS error message when i try to load it.
#       Unrelated to the other app.

import json 
from flask import Flask, request 
from pathlib import Path
from preprocessorSDWAN import load_data, parse_data
import requests 
 
app = Flask(__name__)

# 6/28: Will import an API file upload eventually, but i'm going to leave it alone for now.  
yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml")
# Sun 6/26: doublecheck that clarifying the path as /templates is neccesary/functional  
sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_v3.jinja2")

loaded_data = {} 

# from an earlier build
to_temp_dict = {}

@app.route('/')
def home():
    return "Proof of Concept for Swiftdoc preproc/template engine -currently nonfunctional."
 
# This function will take all that "file upload" crap malarkey showed me 
# then process. 
@app.route('/from-gui', methods=['GET','POST'])
def fromgui():
    if request.method == 'POST':
        # PLACEHOLDER.  In final version it loads from GUI/ API. 
        # 6/28:  It's going to be able to receive a bunch of crap from 
        loaded_data['raw_data'] = load_data(yaml_raw)
        # Below data will be supplied by the API/GUI, but how?
        # New fields in the YAML file? Or is yaml file just part of json/a dict?
        loaded_data['product'] = request.form['product'] 
        loaded_data['replacement_values'] = request.form['replacement_values']
        loaded_data['gdoc_type'] = request.form['gdoc_type']

        # 6:29: going to exclude this for now to remove unncessary compelxity 
        # parsed_data = parse_data(loaded_data['raw_data'])
        # will eventually run an error check. 
        # Anton 6/28:  the data that gets 'returned' is used by
        #               the next method in the process. 
        #     
        #   C
        # Anton: "And that data is what's use din the next method

        # ??????? but this is just gonna send it back to the poster.....
        # 6/28: what if I just put a post call to the template API right here? 
        # What then?? 
        
        # 6/29: Changing this to just return the raw yaml data, as that's all we're giong to be 
        #       able to process until I figure out Ruben's (or someone else's) file uploads thru APIs.
        
        # payload = loaded_data

        # 6/29: processing the post request (or whatever) from the GUI
        # now triggers a post request to the template engine
        url = 'http://127.0.0.1:8000/from-preprocessor'

        # 6/28: can i just use the flask version?
        # how does it differ?
        # drat = requests.post(url, data=payload)
        
        # 6/28: still not completely sure why we're doing this but ok
        # 6/28: ...unless there is a separate way to access the return from a POST requset.... 
        return loaded_data  
    if request.method == 'GET': 
        return "Placeholder (fromgui)"
 
 
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)