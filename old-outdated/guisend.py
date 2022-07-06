# Sim of the GUI sending the yaml data. 
import json 
from flask import Flask, request 
from pathlib import Path 
import requests 
 
# 6/29:  Can't actually send yaml data til I figure out the file upload stuff Ruben showed me 
# 6/29: 	(or figure out how to do this some other way)

# 6/29:  Because the API-wrapped functions that will receive this request are written to 
# 		 process yaml for now, not a full payload. 

# yaml_raw = Path(r"C:\Users\estahl\projects\SDWAN-api-poc\newraw_data.yaml")

# 7/1 - it should be sending the request sa a file upload .


url = "http://127.0.0.1:5000/from-gui"

payload = {
	'product': 'sd-wan',
	'replacement_values': 'more like replaceHOLDER values amirite??',
	'gdoc_type': True
}

requests.post(url, data=payload)

# print(response.text)
