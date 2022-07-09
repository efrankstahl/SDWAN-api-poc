# when it gets to templating engine you wanna dELETE THE RAW DATA FROM THE OBJECt, 
# AND ONLY SEND THE DOC_OUTLINE, just .pop it off. 
# 7/8:  

# TODO: Remove unnecessary libraries.
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

""" Logger initialization. """
tag = {'app_name': 'Templating Engine'} 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(r'services\template-engine\template-engine-log.txt')
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - [ %(app_name)s ] -  %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# Disable stdout printout in live version?
logger.addHandler(stdout_handler)

logger = logging.LoggerAdapter(logger, tag)
""" End logger initialization. """
# 7/8: TODO: Confirm relative path is functional. 
sdwan_template = Path(r"services\template-engine\templates\doc_v4.jinja2")
""" Additional template paths for later use"""
# panos_template = Path('placeholder')
# vmseries_template = Path('placeholder')

 
# TODO: Check if necessary.
raw_incoming = {} 
doc_outline = []
 
@app.route('/')
def homepage():
    return "Template engine homepage."

@app.route('/templating-engine', methods=['GET','POST']) 
def frompreprocessor():
    if request.method == 'POST':
        # 7/7:  evidently, request.json saves the json content as a dictionary object? cool cool cool.
        raw_incoming = request.json 

        # List of allowed products.
        product_list = ['sdwan', 'panos', 'vmseries']
        if raw_incoming['product'].lower() not in product_list:
            resp = jsonify({'Failure': 'Unknown product type.'})
            resp.status_code = 400
            logger.error('Product type {} not in allowed product list.'.format(raw_incoming['product']))
            return resp
        # TODO: Check for missing 'product' field.
        elif raw_incoming['product'] == 'sdwan':
            template_path = sdwan_template
            logger.info("SD-WAN template selected")
        
        else:
            resp = jsonify({'Failure': 'Unknown error when reading product type.'})
            logger.error("Unknown exception occurred when parsing product type.")
            return resp    
        # FUTURE: add different assignments for product types. 
        '''
        elif raw_incoming['product'].lower() == 'panos':
            template_path = panos_template
        elif raw_incoming['product'].lower() == 'vmseries':
            template_path = vmseries_template
        '''


        logger.info("passing request.json: {}".format(type(request.json)))
        # request.data is the raw bytestream?
        # request.json returns a DICTIONARY, not a string? 

        logger.debug('print raw_incoming[product]: {}'.format(raw_incoming['product']))
 
        
        # 7/6: Do we still have to use json.loads on create_doc outline?
        
        doc_outline = create_doc_outline(raw_incoming['parsed_data'], template_path.read_file())
         
        # confirm that format of doc_outline is a list: 
        logger.info('Type of doc_outline should be a list: {}'.format(type(doc_outline))) 
        logger.debug('contents of doc_outline: {}'.format(doc_outline))
        # 7/7 TODO: remove the non-config data before you send it on. 
        '''
        payload = {
            'doc_outline': doc_outline,
            'doc_name': doc_name,
            'gdoc_selected': gdoc_selected,
            'init_id': init_id,
            'replacement_values': replacement_values
        }

        response = requests.post('http://127.0.0.1:8000/doc-engine', json=payload)
        print("A POST request containing the document outline has been sent.")
        return response.content, response.status_code
'''
        resp = 'Placeholder.'
        return resp  


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

 