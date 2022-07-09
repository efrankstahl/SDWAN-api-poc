
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
 

# We'll define the paths to a bunch fo template strings at the top of the file!
def create_doc_outline(data, template_str):
    template = jinja2.Template(template_str, trim_blocks=True)
    initial_outline = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    doc_outline = ast.literal_eval(initial_outline)
    return doc_outline 
 
 