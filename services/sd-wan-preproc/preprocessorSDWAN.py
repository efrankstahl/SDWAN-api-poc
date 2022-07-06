# 7/6: I am currenly not using any of these functions in the api, so... 
# unless I refactor some stuff into functions, this isn't needed. 
from dataclasses import dataclass
from unipath import Path
from jinja2 import Template
import json
import jinja2
import re 
import requests
import yaml
 

# 7/5 this needs to be changed for use in the new preprocessor. 

def load_data(yaml_file):
    with open(yaml_file, "r") as file:
        loaded_data = yaml.load(file, yaml.FullLoader)
    return loaded_data
 
#  just purely return the loaded data, in case people have to add methods later
def parse_data(loaded_data):
    return loaded_data

# this is a python dictionary 
# full_data = load_data(yaml_raw)
 
# 6/29: Is this breaking something? We'll have to change this anyhow.
# Sends processed data to the API 
#url = 'http://127.0.0.1:5000/to-template'

# 6/28 REMOVE PROBABLY
payload = {
    'raw_data': full_data,
    'product': 'SD-WAN',
    'replacement_values': '[ PLACEHOLDER FOR THE DOC ENGINE ]',
    'gdoc_type': True
}

#response = requests.post(url, data=payload)
 


'''
API_VALUES_RECEIVED = {
    'raw_data': 'the yaml file with all the data',
    'product': 'SD-WAN', 
    'replacement_values':  <for the doc engine; we don't really have to care>
    'gdoc_type':  true
}
API_VALUES_PUSHED = {
    # aka the ones we send to template eng
    'parsed_data': 'this will be the document outline as a list',
    'product': 'SD-WAN',
    'replacement_values': '<who cares>',
    'gdoc_type': True
}
'''
