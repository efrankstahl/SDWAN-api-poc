
from dataclasses import dataclass
from unipath import Path
import json
import jinja2
from jinja2 import Template
import requests
import re 
import yaml

'''This file would not feature in the real code'''
''' It is just a test that everything is processing together.'''


yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-tire-kicking\raw_data.yaml")


sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_v2.jinja2") 

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

def load_data(yaml_file):
    with open(yaml_file, "r") as file:
        loaded_data = yaml.load(file, yaml.FullLoader)
    return loaded_data
 
#  just purely return the loaded data, in case people have to add methods later
def parse_data(loaded_data):
    return loaded_data

# this is a python dictionary 
full_data = load_data(yaml_raw)
# print(full_data)

# 6/28: works til this point

# Now testing the create_doc_outline function 
# with raw_data.yml + doc_v2.jinja2
def create_doc_outline(data, template_str):
    template = jinja2.Template(template_str, trim_blocks=True)
    doc_outline = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    return doc_outline 

# Ruben's note: If I don't include .read_file(), it will try to run this with just the Path, 
# not the actual contents of the path. 
doc_outline = create_doc_outline(load_data, sdwan_template.read_file())
# 6/28: why is it a string that just contains the path to the 
print(type(doc_outline))