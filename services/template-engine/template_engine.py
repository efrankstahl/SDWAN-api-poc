
import ast
from dataclasses import dataclass
from unipath import Path
import json
import jinja2
from jinja2 import Template
import logging 
import requests
import re 
import sys
import yaml


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')


# Template paths for diff engines
# (Functionality to be added later.) 
'''
file_directory = Path('debug_output/')
panos_template = Path('panos_doc.jinja2')
'''
sdwan_template = Path('doc_v4.jinja2')
# 6/23 API: This has to receive the API data 
# 6/23 API: AND IT WILL SEND THE DOCUMENT OUTLINE AS A LIST (like JSON, but a python object)


class TableCount(object):
    def __init__(self, start_value=1):
        self.value = start_value

    def current(self):
        return self.value

    def next(self):
        v = self.value
        self.value += 1
        return v 


def j_dumps(raw_text):
    if isinstance(raw_text, (int, type(None))):
        raw_text = str(raw_text)
    json_txt = json.dumps(raw_text)
    return json_txt
 

# 6/24: Ruben's function from the video on the 21st:
# (the flask api WILL CALL THIS FUNCTION)
# 'template str' being --we'll define the paths to a bunch fo template strings at the top of the file!
def create_doc_outline(data, template_str):
    template = jinja2.Template(template_str, trim_blocks=True)
    initial_outline = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    doc_outline = ast.literal_eval(initial_outline)
    return doc_outline 

# oh ho!! in the new version this function will take the result of the api call as input.  
# results_dict = load_data(r"C:\Users\estahl\projects\SDWAN-tire-kicking")

#create_doc_outline(results_dict)
'''
API_VALUES_RECEIVED = {
    'parsed_data': 'the dictionary from the preprocessor',
    'product': 'SD-WAN', 
    'replacement_values':  <for the doc engine; we don't really have to care>
    'gdoc_type':  true
}
API_VALUES_PUSHED = {
    # aka the ones we send to template eng
    'docu_outline: 'this will be the document outline as a list', (like a json-style list of dictionaries!)
    'product': 'SD-WAN',
    'replacement_values': '<who cares>',
    'gdoc_type': True
}
'''
