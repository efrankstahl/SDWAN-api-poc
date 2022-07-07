# when it gets to templating engine you wanna dELETE THE RAW DATA FROM THE OBJECt, 
# AND ONLY SEND THE DOC_OUTLINE, just .pop it off. 

import json 
from flask import Flask, request 
from unipath import Path 
import jinja2
from jinja2 import Template
from template_engine import create_doc_outline, j_dumps
from template_engine import TableCount
import requests
import re
import yaml

app = Flask(__name__)
 
sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_4.jinja2")
 

 
raw_incoming = {} 
doc_outline = []
 
@app.route('/')
def homepage():
    return "Template engine homepage."

@app.route('/from-preprocessor', methods=['GET','POST'])
# 6/28:  let's just see if it can receive the post request before we do anything fancy. 
# 7/1 : Is THIS where the file upload stuff becomes relevant. 
    
def frompreprocessor():
    if request.method == 'POST':
        # this is FLASK'S requet method
        raw_incoming = request.json
        # raw_incoming['raw_data'] = request.form['raw_data']
        # raw_incoming['product'] = request.form['product']
        # raw_incoming['replacement_value'] = request.form['replacement_values']
        # raw_incoming['gdoc_type'] = request.form['gdoc_type']

        # 6/30, evening: let's fill in ALL this data, and then put the raw_data key in the 
        #       function call

        # 6/30: returns a list.  note it will ONLY need to prcess the
        # config information, nothing else.  
 
        # 7/6: Do we still have to use json.loads on create_doc outline?
        # doc_outline = create_doc_outline(raw_incoming['raw_data'], sdwan_template.read_file())




        # FINAL RESULT IS A LIST.
        # print(type(doc_outline))
        # 6/30: make a post request to doc engine?
        return raw_incoming
        # unpack data from the POST request
        # (eventually) check that it's SDWAN
        # run create_doc_outline on it 
        # 6/29:  !! Make sure your create doc outline functions like
        #        it does in testprocessing.py!
    if request.method == 'GET':
        if not raw_incoming:
            return "Haven't received any post data from the preprocessor yet..."
        else:
            return raw_incoming
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)