from dataclasses import dataclass
from unipath import Path
import json
import jinja2
import re

file_directory = Path('debug_output/')
# print(file_directory.listdir())

# counter object for jinja
# resolves some issue with jinja. don't wrry aobu it. around 13:00
class TableCount(object):
    def __init__(self, start_value=1):
        self.value = start_value

    def current(self):
        return self.value

    def next(self):
        v = self.value
        self.value += 1
        return v

# resolves issues with the googleAPI/jinja tepmlate
# you can't use plain old json.dumps like you can json.loads (nin this program)
def j_dumps(raw_text):
    if isinstance(raw_text, (int, type(None))):
        raw_text = str(raw_text)
    json_txt = json.dumps(raw_text)
    return json_txt

''' 
def parse_data(files_path):
    parsed_data ={}
    for file_item in file_directory.listdir():
        # key: filename value: objectified json data from that file
        parsed_data[file_item.stem] = json.loads(file_item.read_file())
    print(parsed_data)
    return parsed_data
# we might have to change this from reading a dir to unzipping a zipfile etc
'''

# this currently handles only json; we need to run a check for if it'll handle
# YAML... we could use the .ext proprety (file_item.ext) to check what it is.

# read all the data from the Zip file and create a dictionary with the file name as the keys

def load_data(files_path):
    loaded_data = {}
    for file_item in file_directory.listdir():
        loaded_data[file_item.stem] = json.loads(file_item.read_file())
    return loaded_data

#  maybe after i load data, have it go thru this parse data thing 
#  just purely return the loaded data, in case people have to add methods later
def parse_data(loaded_data):
    return loaded_data


def create_doc_outline(data):
    template_path = Path('doc.jinja2')
    template = jinja2.Template(template_path.read_file(), trim_blcks=True)
    # all these args are so the function knows to use those other functions/objs
    # they're mostly to make sure the jinja is handled correctly
    # Ruben goes into detail around ~12-16
    doc_outline = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    # double check that data=data still wroks above.
    return doc_outline

# 1.  You will receive a zip file
# 2.  Unzip file
# 3.  Determine whether the dox are json or yaml and load data into a dictionary 
#       with file_name as the key.
# 4.  Delete zip file
# 5.  Create the Document Outline using the doc.jinja2 and the loaded data
# 6.  Send Document Outline to Template Engine 