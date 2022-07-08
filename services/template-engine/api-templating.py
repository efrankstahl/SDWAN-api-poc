# when it gets to templating engine you wanna dELETE THE RAW DATA FROM THE OBJECt, 
# AND ONLY SEND THE DOC_OUTLINE, just .pop it off. 


# 7/7:  Keeping all libraries for now until refactoring is complete.
import json 
from flask import Flask, jsonify, request 
import jinja2
from jinja2 import Template
import logging
from template_engine import create_doc_outline, j_dumps
from template_engine import TableCount
import requests
import re
import sys
from unipath import Path 
import yaml

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(asctime)s -  %(levelname)s -  %(message)s')
logging.disable(logging.DEBUG)

# 7/7: Change path before final version. 
sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_v4.jinja2")
# panos_template = Path()
# vmseries_template = Path()

 
# TODO: Check if necessary.
raw_incoming = {} 
doc_outline = []
 
@app.route('/')
def homepage():
    return "Template engine homepage."

@app.route('/from-preprocessor', methods=['GET','POST']) 
# 7/7: create doc outline. 
def frompreprocessor():
    if request.method == 'POST':
        # 7/7:  Work starts here. 
        # 7/7:  evidently, request.json saves the json content as a dictionary object? cool cool cool.
        raw_incoming = request.json
        # 7/7: TODO: check what the product is and select template.

        # List of allowed products.
        product_list = ['sdwan', 'panos', 'vmseries']
        if raw_incoming['product'].lower() not in product_list:
            resp = jsonify({'Failure': 'Unknown product type.'})
            resp.status_code = 400
            logging.error('Product type {} not in allowed product list.'.format(raw_incoming['product']))
            return resp
        # TODO: Check for missing 'product' field.
        elif raw_incoming['product'] == 'sdwan':
            template_path = sdwan_template
            logging.info("[ SD-WAN template selected ]")
        # FUTURE: add different assignments for product types. 
        '''
        elif raw_incoming['product'].lower() == 'panos':
            template_path = panos_template
        elif raw_incoming['product'].lower() == 'vmseries':
            template_path = vmseries_template

        else:
            resp = jsonify({'Failure': 'Unknown error when reading product type.'})
            logging.error("Unknown exception occurred when parsing product type.")
            return resp
        '''
        logging.info("passing request.json: {}".format(type(request.json)))
        # request.data is the raw bytestream?
        # request.json returns a DICTIONARY, not a string? 

        # 7/7:  raw_incoming['product'] returns successfully
        logging.debug('print raw_incoming[product]: {}'.format(raw_incoming['product']))
 
        
        # 7/6: Do we still have to use json.loads on create_doc outline?
        
        # TODO: Get create_doc_outline to work! 

        doc_outline = create_doc_outline(raw_incoming['yaml_data'], template_path.read_file())
         
        # confirm that format of doc_outline is a list: 
        logging.info('Type of doc_outline should be a list: {}'.format(type(doc_outline))) 
        logging.debug('contents of doc_outline: {}'.format(doc_outline))
        # 7/7 TODO: remove the non-config data before you send it on. 
        resp = 'Placeholder.'
        return resp  

    # TODO: Remove. 
    if request.method == 'GET':
        if not raw_incoming:
            return "Haven't received any post data from the preprocessor yet..."
        else:
            return raw_incoming
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

 