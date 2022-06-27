from dataclasses import dataclass
from unipath import Path
import json
import jinja2
import re 
# 1.  You will receive a zip file
# 2.  Unzip file
# 3.  Determine whether the dox are json or yaml and load data into a dictionary 
#       with file_name as the key.
# 4.  Delete zip file
# 5.  Create the Document Outline using the doc_v2.jinja2 and the loaded data
# 6.  Send Document Outline to Template Engine  

# this originally had a debugger as an argument
# HEY --
file_directory = Path(r"C:\Users\estahl\projects\SDWAN-tire-kicking\Sample-unzipped")
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
# you can't use plain old json.dumps like you can json.loads (in this program)
def j_dumps(raw_text):
    if isinstance(raw_text, (int, type(None))):
        raw_text = str(raw_text)
    json_txt = json.dumps(raw_text)
    return json_txt

# !!! Ruben added this API basic stuff 6/21 meeting
# Here's where ruben showed us how to set up 'expected API values'
# (note it doesn't have to be set up 'exactly' like this)

 
'''
# ON A REWATCH, THIS COMES FROM THE GUI: 
API_VALUES_RECEIVED = {
    'raw_data': 'The File/Folder with all the data',
    'product': 'SD-WAN', 
    'replacement_values':  <for the doc engine; we don't really have to care>
    'gdoc_type':  true
}
API_VALUES_PUSHED = {
    # aka the ones we send
    'parsed_data': 'this will be the document outline as a list',
    'product': 'SD-WAN',
    'replacement_values': '<who cares>',
    'gdoc_type': True
}
'''
'''
API_VALUES_PUSHED = {
    # aka the ones we send
    'parsed_data': 'this will be the parsed data as a list',
    'product': 'SD-WAN',
    'replacement_values': '<who cares>',
    'gdoc_type': True
}'''

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

# 6/22: previously he said we'd be unzippig a zip file but now it looks like we're
# receiving an api call with a json document. 
 
#  maybe after i load data, have it go thru this parse data thing 
#  just purely return the loaded data, in case people have to add methods later



file_directory = Path(r"C:\Users\estahl\projects\SDWAN-tire-kicking\Sample-unzipped")

def load_data(files_path):
    loaded_data = {}
    for file_item in file_directory.listdir():
        # turning the json into a python dict
        # we'll also have to do a check for json vs yaml and handle it appropriately
        loaded_data[file_item.stem] = json.loads(file_item.read_file())
    return loaded_data

def parse_data(loaded_data):
    return loaded_data

def create_doc_outline(data):
    # 6/24 : changed to the new jinja template, but....
    template_path = Path('./templates/doc_v2.jinja2')
    template = jinja2.Template(template_path.read_file(), trim_blocks=True)  
    # all these args are so the function knows to use those other functions/objs
    # they're mostly to make sure the jinja is handled correctly
    # Ruben goes into detail around ~12-16
    # WHAT IS HAPPENING HERE IN THIS LINE.
    doc_outline = template.render(data=data, j_dumps=j_dumps, j_loads=json.loads, TableCount=TableCount, re=re)
    return doc_outline

loaded_data = load_data(file_directory)
testy = create_doc_outline(loaded_data) 

print(type(testy))
# 6/24: i no longer get an error, but the result of create_doc_outline is now a blank streing
print(testy)

