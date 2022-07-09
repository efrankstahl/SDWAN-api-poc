# 7/6: I am currenly not using any of these functions in the api, so... 
# unless I refactor some stuff into functions, this isn't needed. 

from unipath import Path
from jinja2 import Template
import json
import jinja2
import logging 
import re 
import requests
import sys
import yaml


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -  %(levelname)s -  %(message)s')

# 7/5 this needs to be changed for use in the new preprocessor. 

'''
def load_data(yaml_file):
    with open(yaml_file, "r") as file:
        loaded_data = yaml.load(file, yaml.FullLoader)
    return loaded_data
'''

#  just purely return the loaded data, in case people have to add methods later
def parse_data(loaded_data):
    return loaded_data

