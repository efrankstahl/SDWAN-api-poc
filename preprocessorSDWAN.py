# Just the functions we need to set up the preprocessy bit
# this is the pre-processor for SD-WAN, specifically

from dataclasses import dataclass
from unipath import Path
from jinja2 import Template
import json
import jinja2
import re 
import requests
import yaml

# TEMPORARY 
# from template_engine import create_doc_outline

# eventually this will have to receive an API 
# 6/24 for now we gotta make it take a single yaml file instead of going thru a directory.
# 6/24 ! we can make a sendgui.py that sends the yaml file thru api 
yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-tire-kicking\raw_data.yaml")


# open the yaml file and make it a dictionary
# eventually i'll be receiving yaml from a GUI/API 
def load_data(yaml_file):
    with open(yaml_file, "r") as file:
        loaded_data = yaml.load(file, yaml.FullLoader)
    return loaded_data
 
#  just purely return the loaded data, in case people have to add methods later
def parse_data(loaded_data):
    return loaded_data

# this is a python dictionary 
full_data = load_data(yaml_raw)
 

# Sends processed data to the API 
url = 'http://127.0.0.1:5000/to-template'

payload = {
    'raw_data': full_data,
    'product': 'SD-WAN',
    'replacement_values': '[ PLACEHOLDER FOR THE DOC ENGINE ]',
    'gdoc_type': True
}

response = requests.post(url, data=payload)
 


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
