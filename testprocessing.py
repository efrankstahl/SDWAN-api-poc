
from dataclasses import dataclass
from unipath import Path
import ast
import json
import jinja2
from jinja2 import Template
import requests
import re 
import yaml

'''This file would not feature in the real code'''
''' It is just a test that everything is processing together.'''


yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml")


sdwan_template = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\services\template-engine\templates\doc_v4.jinja2") 

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
# with raw_data.yml + doc_v3.jinja2
# 6/30: This function accepts a dictionary and a path.
def create_doc_outline(data, template_str):
    template = jinja2.Template(template_str, trim_blocks=True)
    outline_string = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    doc_outline = ast.literal_eval(outline_string)
    return doc_outline 

# Ruben's note: If I don't include .read_file(), it will try to run this with just the Path, 
# not the actual contents of the path. 

doc_outline = create_doc_outline(full_data, sdwan_template.read_file())


# 6/30: error resolved
#print(doc_outline)
# 6/29: It's a string
print(type(doc_outline))

print(doc_outline[0])
print("Doc_outine is datatype ", type(doc_outline))
# 6/30 : already created this file of doc_outltine output.
#file = open('filled_template.txt', 'w')
#file.write(doc_outline)